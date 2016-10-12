import os
import yaml
import time
import schedule

"""
This script create a linux command from settings.yaml. This linux command backup the database or restore it.
in settings.yaml, if wanted_tables has only -None then all the database is backupped. Otherwise it just
backup or restore the tables under wanted_tables.
"""


def create_essentials():
    yaml_file = open("settings.yaml", 'r')
    settings = yaml.load(yaml_file)
    db_name = settings["db_name"]
    db_user = settings["db_user"]
    db_password = settings["db_password"]
    db_host = settings["db_host"]
    db_port = settings["db_port"]
    backup_path = settings["backup_path"]
    filename = settings["filename"]
    table_names = settings["tables"]
    wanted_tables = settings["wanted_tables"]
    filename = filename + "-" + time.strftime("%Y%m%d") + ".backup"
    command_str = str(db_host)+" -p "+str(db_port)+" -d "+db_name+" -U "+db_user
    return command_str, backup_path, filename, table_names, wanted_tables


def backup_database():
    command_str, backup_path, filename, all_table_names, wanted_tables = create_essentials()
    command_str = "pg_dump -h "+command_str

    if wanted_tables[0] != "None":
        for x in wanted_tables:
            command_str = command_str +" -t "+x

    command_str = command_str + " -F c -b -v -f '"+backup_path+"/"+filename+"'"

    try:
        os.system(command_str)
        print "Backup completed"
    except Exception as e:
        print "!!Problem occured!!"
        print e


def restore_database():
    command_str, backup_path, filename, all_table_names, wanted_tables = create_essentials()
    command_str = "pg_restore -h "+command_str

    if wanted_tables[0] != "None":
        for x in wanted_tables:
            command_str = command_str +" -t "+x

    command_str = command_str + " -v '"+backup_path+"/"+filename+"'"
    try:
        os.system(command_str)
        print "Restore completed"
    except Exception as e:
        print "!!Problem occured!!"
        print e


def main():
    schedule.every().day.at("17:06").do(backup_database)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
