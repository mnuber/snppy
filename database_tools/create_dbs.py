from snpadapter import SNPAdapter
        
def setup_snp_db(filename):

    #DNA is the table containing user DNA data (formerly snppy)
    sql = """CREATE TABLE dna (dna_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dna_rsid CHAR(40), dna_chrom CHAR(40), dna_pos INT, dna_gen CHAR(2));
    CREATE TABLE snpedia (snpedia_id INTEGER PRIMARY KEY AUTOINCREMENT,
    snpedia_rsid CHAR(40), snpedia_gen CHAR(40), snpedia_mag INT, snpedia_repute CHAR(20), snpedia_notes TEXT);
    CREATE TABLE snp_groups (grp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    grp_gid CHAR(40), grp_notes TEXT);
    CREATE TABLE grp_data (grp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    grp_rsid CHAR(40), snp_grp_gid CHAR(40), grp_gen CHAR(2));
    """

    snpdb = SNPAdapter.SNPAdapter(filename)
    snpdb.create_table(sql)
    print filename + " database was created."
    snpdb.commit_and_close()

class DNA(object):

    def __init__(self, rsid, chromosome, position, genotype):
        self.rsid = rsid
        self.chromosome = chromosome
        self.position = position
        self.genotype = genotype

    def get_database_object(self):
        return (self.rsid, self.chromosome, self.position, self.genotype)
        
def setup_dna_db(dna_file, db_file):
    snpdb = SNPAdapter.SNPAdapter(db_file)
    snpdb.set_table('dna')
    snpdb.columns = snpdb.dna_columns
    dnaList = list()
    try:
        fdna = open(dna_file, 'rb')
        for entry in fdna:
            print entry
            if entry.find("#") is -1:
                entry = entry.split("\t")
                dnaList.append(DNA(entry[0],entry[1],entry[2],entry[3].rstrip("\n").rstrip("\r")))
        
    except IOError as e:
            print e
            print "Make sure " + dna_file + " is the correct file."

    count = 0
    for dna_entry in dnaList:
        count = count + 1
        snpdb.insert(dna_entry.get_database_object())
    
    
    print dna_file + " was processed, " + str(count) + " entries in " + db_file + " were updated."
    snpdb.commit_and_close()

