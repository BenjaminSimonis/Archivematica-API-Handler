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
    return

def command_description(command):
    if command == "start_transfer":
        pass
    elif command == "list_unapproved":
        pass
    elif command == "approve_transfer":
        pass
    elif command == "status_transfer":
        pass
    elif command == "completed_transfer":
        pass
    elif command == "hide_transfer":
        pass
    elif command == "status_ingest":
        pass
    elif command == "hide_ingest":
        pass
    elif command == "waiting_ingests":
        pass
    elif command == "completed_ingest":
        pass
    elif command == "full_reingest":
        pass
    elif command == "part_reingest":
        pass
    else:
        raise SyntaxError('Use one of the documented keywords!')
