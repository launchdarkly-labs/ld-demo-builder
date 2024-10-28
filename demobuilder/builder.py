import os
import sys
import randomname
import FinTechBuilder
import UserProfileBuilder

LD_API_KEY = os.environ["LD_API_KEY"]
LD_API_KEY_USER = ""

if "LD_API_KEY_USER" in os.environ:
    LD_API_KEY_USER = os.environ["LD_API_KEY_USER"]


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
        if len(sys.argv) < 2:
            print(
                "Usage: python builder.py build <project-key=PROJECT_KEY> <email=EMAIL_ADDRESS> <custom-name=CUSTOM_NAME> <demo-type=DEMO_TYPE>"
            )
            sys.exit()

        project_key = ""
        project_name = ""
        email = ""
        custom_name = ""
        demo_type = ""
        demo = None

        for arg in sys.argv[2:]:
            items = arg.split("=")
            match items[0].lower():
                case "project-key":
                    project_key = items[1].lower()
                case "email":
                    email = items[1].lower()
                case "custom-name":
                    custom_name = items[1]
                case "demo-type":
                    demo_type = items[1].lower()

        if email == "":
            print("Error: Missing email address.")
            sys.exit()

        pname = randomname.get_name().lower()
        if custom_name == "":
            project_name = "Coast Demo (" + pname + ")"
        else:
            project_name = custom_name

        create_project = False
        if project_key == "":
            create_project = True
            project_key = "cxld-" + pname
        else:
            project_name = "Coast Demo (" + project_key.replace("cxld-", "") + ")"

        match demo_type:
            case "userprofile":
                demo_type = "UserProfile"
                demo = UserProfileBuilder.UserProfileBuilder(
                    LD_API_KEY, email, LD_API_KEY_USER, project_key, project_name
                )
            case _:
                demo_type = "FinTech"
                demo = FinTechBuilder.FinTechBuilder(
                    LD_API_KEY, email, LD_API_KEY_USER, project_key, project_name
                )

        # will eventually be: build_all()
        if create_project:
            demo.create_project()
        else:
            demo.project_created = True

        demo.build()

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
        email = "kcochran@launchdarkly.com"
        demo = FinTechBuilder.FinTechBuilder(
            LD_API_KEY, email, LD_API_KEY_USER, project_key, project_name
        )
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
