#!/usr/bin/python
from .. import versioning
import sys
if sys.version_info[0] == 3:
    from sqlite3 import dbapi2
else:
    from pyspatialite import dbapi2
import psycopg2
import os
import shutil
import tempfile

if __name__ == "__main__":
    test_data_dir = os.path.dirname(os.path.realpath(__file__))
    tmp_dir = tempfile.gettempdir()

    # create the test database

    os.system("dropdb epanet_test_db")
    os.system("createdb epanet_test_db")
    os.system("psql epanet_test_db -c 'CREATE EXTENSION postgis'")
    os.system("psql epanet_test_db -f "+test_data_dir+"/epanet_test_db_unversioned.sql")

    versioning.historize("dbname=epanet_test_db","epanet")

    # try the update
    wc = tmp_dir+"/bug_in_branch_after_commit_wc.sqlite"
    if os.path.isfile(wc): os.remove(wc) 
    versioning.checkout("dbname=epanet_test_db", ['epanet_trunk_rev_head.junctions', 'epanet_trunk_rev_head.pipes'], wc)

    scur = versioning.Db( versioning.spatialite_connect( wc ) )

    scur.execute("SELECT * FROM pipes")
    scur.execute("UPDATE pipes_view SET length = 1 WHERE OGC_FID = 1")
    scur.commit()

    versioning.commit(wc,'test', "dbname=epanet_test_db" )

    versioning.add_branch("dbname=epanet_test_db","epanet","mybranch","add 'branch")
