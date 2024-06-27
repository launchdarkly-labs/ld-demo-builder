import os
import sys
import randomname
import DemoBuilder


LD_API_KEY = os.environ["LD_API_KEY"]


def usage():
    print("Usage: python builder.py COMMAND")
    print("Commands:")
    print("  build")
    print("  cleanup <project_key>")
    print("Example:")
    print("  python builder.py build")
    sys.exit()


if len(sys.argv) < 2:
    usage()

cmd = sys.argv[1].lower()

match cmd:
    case "build":
        project_key = ""
        project_name = ""
        create_project = False
        if len(sys.argv) == 2:
            create_project = True
            pname = randomname.get_name()
            project_key = "cxld-" + pname
            project_name = "Coast Demo (" + pname + ")"
        else:
            project_key = sys.argv[2].lower()
            project_name = "Coast Demo (" + project_key.replace("cxld-", "") + ")"

        demo = DemoBuilder.DemoBuilder(LD_API_KEY, project_key, project_name)
        # will eventually be: build_all()
        if create_project:
            demo.create_project()
        else:
            demo.project_created = True

        demo.create_flags()
        demo.create_metrics()
        demo.create_metric_groups()
        # demo.create_experiments()
        demo.run_experiment()
        print(
            "Project created: "
            + project_name
            + " (Project Key is: "
            + project_key
            + ")"
        )
        print("Client-side SDK key: " + demo.client_id)
        print("Server-side SDK key: " + demo.sdk_key)
    case "cleanup":
        if len(sys.argv) < 3:
            print("Usage: python builder.py cleanup <project_key>")
            sys.exit()
        pname = sys.argv[2].lower()
        if not pname.startswith("cxld-"):
            print("Error: This does not appear to be a Coast demo project.")
            sys.exit()
        project_key = pname
        project_name = "Coast Demo (" + pname.replace("cxld-", "") + ")"
        demo = DemoBuilder.DemoBuilder(LD_API_KEY, project_key, project_name)
        print(
            "Are you sure you want to delete this project? It will be gone forever and cannot be undone."
        )
        confirm = input("Type 'DELETE' to confirm: ")
        if confirm == "DELETE":
            demo.cleanup()
        else:
            print("Project not deleted.")
    case _:
        usage()
