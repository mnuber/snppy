from sqliteutils import SQLAdapter

##SNPAdapter is derived from SQLAdapter.
##It is a concrete class for performing CRUD updates on the 23andme/snpedia data

class SNPAdapter(SQLAdapter.SQLAdapter):

    dna_columns = ('dna_rsid','dna_chrom', 'dna_pos', 'dna_gen')
    snpedia_columns = ('snpedia_rsid','snpedia_gen', 'snpedia_mag', 'snpedia_repute'  , 'snpedia_notes')
    snp_groups_columns = ('grp_gid', 'grp_notes')
    grp_data_columns = ('grp_rsid', 'snp_grp_gid', 'grp_gen')
    
    def __init__(self,filename):
        super(SNPAdapter, self).__init__(filename)



    
