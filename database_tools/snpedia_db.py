import json
import urllib
import mwparserfromhell as pfh
from snpadapter import SNPAdapter
import create_dbs
import cPickle

class SNPediaEntry(object):

    def __init__(self, rsid):
        self.snp = dict()
        self.parse_snp(rsid)
 
    def parse(self, rsid):
        data = {"action": "query", "prop": "revisions", "rvlimit": 1,
                "rvprop": "content", "format": "json", "titles": rsid}
        try:
            snpDict = json.loads(urllib.urlopen("http://bots.snpedia.com/api.php", urllib.urlencode(data)).read())
        except IOError as ioe:
            print ioe
            return None
        try:
            text = snpDict["query"]["pages"].values()[0]["revisions"][0]["*"]
            return pfh.parse(text)
        except KeyError as K:
            return None

    def parse_snp(self, rsid):
        self.snp = self.create_snp_dict(self.get_templates(self.parse(rsid)))
        return self.snp

    def parse_genos(self):
        self.geno = dict()
        self.parse_geno(self.get_geno1())
        self.parse_geno(self.get_geno2())
        self.parse_geno(self.get_geno3())
        
    def parse_geno(self, geno):
        self.geno[geno] = SNPediaEntry(self.get_rsid() + geno)
        return self.geno

    def print_genos(self):
        for item in self.geno:
            print self.get_rsid() + item
            print self.geno[item].get_summary()
            
    def print_snp(self):
        print "============"
        print self.get_rsid()
        print self.get_summary().upper()
        print "------------"
        print '\n'
        self.print_genos()

    def get_templates(self, values):
        if values is not None:
            return values.filter_templates()[0].params
        else:
            return None

    def create_snp_dict(self, templates):
        if templates is not None:
            snps = dict()
            for t in templates:
                entries = t.split("=")
                try:
                    snps[entries[0]] = entries[1].rstrip("\n").encode('ascii')
                except UnicodeEncodeError as u:
                    print u
                    return dict()
            return snps
        else:
            return dict()
        
    def get_rsid(self):
        if self.snp is not None:
            if 'rsid' in self.snp:
                return 'rs' + self.snp['rsid']
            else:
                return 'N/A'

    def get_repute(self):
        if 'repute' in self.snp:
            return self.snp['repute']
        else:
            return 'N/A'
        
    def get_geno1(self):
        if 'geno1' in self.snp:
            return self.snp['geno1']
        else:
            return 'N/A'

    def get_geno2(self):
        if 'geno2' in self.snp:
            return self.snp['geno2']
        else:
            return 'N/A'

    def get_geno3(self):
        if 'geno3' in self.snp:
            return self.snp['geno3']
        else:
            return 'N/A'
        
    def get_mag(self):
        if 'magnitude' in self.snp:
            return self.snp['magnitude']
        else:
            return 'N/A'

    def get_summary(self):
        if 'summary' in self.snp:
            return self.snp['summary']
        else:
            return '-'
        
    def get_geno_object(self):
        return self.geno


class SnpediaDBTools(object):

    def __init__(self, db_file):
        if not self.is_a_db(db_file):
            create_dbs.setup_snp_db(db_file)
            create_dbs.setup_dna_db('../data/private/sample.txt', db_file)
        self.snpdb = SNPAdapter.SNPAdapter(db_file)
        self.snpdb.set_table('snpedia')
        self.snpdb.columns = self.snpdb.snpedia_columns

    def is_a_db(self, db):

        try:
            fdb = open(db, 'rb')
            fileheader = fdb.read(100)
            if fileheader[0:16] == "SQLite format 3\000":
                return True
            else:
                return False
        except IOError as ioe:
            return False
    
    def create_db_object(self, geno, geno_name):
        sql_line = (geno.get_rsid(), geno_name, geno.get_mag(), geno.get_repute(), geno.get_summary())
        return sql_line

    def proc_rsid_from_db(self, rsid):
        snp_entry = SNPediaEntry(rsid)
        snp_entry.parse_genos()
        for entry in snp_entry.get_geno_object():
            self.snpdb.insert(self.create_db_object(snp_entry.get_geno_object()[entry], entry.strip("()").translate(None, ';')))

    def add_rsid_into_db(self, rsid):
            self.snpdb.insert((rsid, '-', '-', '-', '-'))
 

    def commit_and_close(self):
        self.snpdb.commit()
        self.snpdb.close()


    def join_with_two_keys(self, selection, table1, table2, key1, key2, key3, key4):
        return self.snpdb.execute('SELECT DISTINCT ' + selection + ' FROM ' + table1
            + ' AS S CROSS JOIN ' + table2 + ' AS T WHERE S.' + key1 +'=T.' + key2 + ' AND S.'
            + key3 + '=T.' + key4 + ' ORDER BY snpedia_mag DESC' )
    
    def populate_snpedia_table(self):
        x = self.join_with_two_keys('dna_rsid, snpedia_repute, snpedia_notes', 'snpedia', 'dna', 'snpedia_rsid', 'dna_rsid', 'snpedia_gen', 'dna_gen')
        return x

    def get_snpdb(self):
        if self.snpdb is not None:
            return self.snpdb

def setup_snpedia(db_name):
    test = SnpediaDBTools(db_name)

    rsidlist = ('Rs6152', 'rs1333049', 'Rs1000592', 'Rs1000589', 'rs17822931',
               'rs12255372', 'rs333', 'rs1815739')


    print 'Updating SNPs...'
    test.get_snpdb().set_table('snpedia')
    for i in rsidlist:
        test.proc_rsid_from_db(i)
    print 'Completed! Updating database...'
    test.snpdb.commit()
    print 'Done!'
    test.snpdb.close()

def report(db_name):
    test = SnpediaDBTools(db_name)
    print 'Beginning report...'
    report = test.populate_snpedia_table()
    for item in report:
        print item
    test.snpdb.close()
