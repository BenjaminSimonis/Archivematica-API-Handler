def list_commands():
    print("start_transfer - Start a new Transfer")
    print("list_unapproved")
    print("approve_transfer")
    print("status_transfer - Check status of transfer with UUID XXXXXXXXX")
    print("completed_transfer - List of completed transfers.")
    print("hide_transfer - Hide transfer with UUID XXXXXXXX")
    print("status_ingest - Check status of ingest with UUID XXXXXXXXX")
    print("hide_ingest - Hide transfer with UUID XXXXXXXX")
    print("waiting_ingests - List ingests waiting for user action")
    print("completed_ingest - List of completed ingests.")
    print("full_reingest")
    print("part_reingest")
    print("\nFor detailed informations about the commands use 'apiHandler.py help {\"command_name\"}'")
    return


def command_description(command):
    if command == "start_transfer":
        print("apiHandler.py start_transfer {'name for transfer'} {'type of transfer'} {'accession number'} {'foldername in source path'}")
        return
    elif command == "list_unapproved":
        print("apiHandler.py list_unapproved")
        return
    elif command == "approve_transfer":
        print("apiHandler.py approve_transfer {'type of transfer'} {'name for transfer'}")
        return
    elif command == "status_transfer":
        print("apiHandler.py status_transfer {'uuid of transfer'}")
        return
    elif command == "completed_transfer":
        print("apiHandler.py completed_transfer")
        return
    elif command == "hide_transfer":
        print("apiHandler.py hide_transfer {'uuid of transfer'}")
        return
    elif command == "status_ingest":
        print("apiHandler.py status_ingest {'uuid of ingest'}")
        return
    elif command == "hide_ingest":
        print("apiHandler.py hide_ingest {'uuid of ingest'}")
        return
    elif command == "waiting_ingests":
        print("apiHandler.py waiting_ingests")
        return
    elif command == "completed_ingest":
        print("apiHandler.py completed_ingest")
        return
    elif command == "full_reingest":
        print("apiHandler.py full_reingest")
        return
    elif command == "part_reingest":
        print("apiHandler.py part_reingest")
        return
    else:
        raise SyntaxError('Use one of the documented keywords!')
