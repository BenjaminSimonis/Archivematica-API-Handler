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
        print("main.py start_transfer {'name for transfer'} {'type of transfer'} {'accession number'} {'foldername in source path'}")
        return
    elif command == "list_unapproved":
        print("main.py list_unapproved")
        return
    elif command == "approve_transfer":
        print("main.py approve_transfer {'type of transfer'} {'name for transfer'}")
        return
    elif command == "status_transfer":
        print("main.py status_transfer {'uuid of transfer'}")
        return
    elif command == "completed_transfer":
        print("main.py completed_transfer")
        return
    elif command == "hide_transfer":
        print("main.py hide_transfer {'uuid of transfer'}")
        return
    elif command == "status_ingest":
        print("main.py status_ingest {'uuid of ingest'}")
        return
    elif command == "hide_ingest":
        print("main.py hide_ingest {'uuid of ingest'}")
        return
    elif command == "waiting_ingests":
        print("main.py waiting_ingests")
        return
    elif command == "completed_ingest":
        print("main.py completed_ingest")
        return
    elif command == "full_reingest":
        print("main.py full_reingest")
        return
    elif command == "part_reingest":
        print("main.py part_reingest")
        return
    else:
        raise SyntaxError('Use one of the documented keywords!')
