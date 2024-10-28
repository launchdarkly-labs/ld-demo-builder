import LDPlatform
import time


class UserProfileBuilder:
    project_created = False
    flags_created = False
    segments_created = False
    metrics_created = False
    metric_groups_created = False
    contexts_created = False
    experiment_created = False
    email = None
    client_id = ""
    sdk_key = ""
    phase_ids = {}

    # Initialize UserProfileBuilder
    def __init__(self, api_key, email, api_key_user, project_key, project_name):
        self.api_key = api_key
        self.email = email
        self.api_key_user = api_key_user
        self.project_key = project_key
        self.project_name = project_name
        self.ldproject = LDPlatform.LDPlatform(api_key, api_key_user, email)
        self.ldproject.project_key = project_key

    def build(self):
        self.create_project()
        self.create_flags()
        self.create_segments()
        self.create_contexts()
        self.create_metrics()
        # self.create_metric_groups()
        self.run_experiment()
        # self.setup_release_pipeline()
        self.update_add_userid_to_flags()
        self.project_settings()

    # Create the project
    def create_project(self):
        if self.project_created:
            return
        print("Creating project", end="...")
        self.ldproject.create_project(self.project_key, self.project_name)
        print("Done")
        self.client_id = self.ldproject.client_id
        self.sdk_key = self.ldproject.sdk_key
        self.project_created = True

    # Create all the flags
    def create_flags(self):
        if not self.project_created:
            print("Error: Project not created")
            return
        print("Creating flags:")
        # AI flags
        print("  - Config: System Prompt")
        self.flag_config_system_prompt()
        print("  - Config: AI Model")
        self.flag_config_ai_model()
        print("  - Release: Chatbot")
        self.flag_rel_chatbot()
        # New UI components
        print("  - Release: Chart")
        self.flag_rel_chart()
        print("  - Release: Gold Upgrade Button")
        self.flag_rel_gold_button()
        print("  - Release: New UI")
        self.flag_rel_new_ui()
        print("  - Release: Fire Overlay")
        self.flag_rel_fire_overlay()
        print("  - Release: Dark Mode")
        self.flag_rel_dark_mode()
        print("  - Release: New Background")
        self.flag_rel_new_background()

        self.ldproject.add_prerequisite_to_flag(
            "release-chatbot", "release-new-ui", 2, "production"
        )
        self.ldproject.add_prerequisite_to_flag(
            "release-chatbot", "release-new-ui", 2, "test"
        )
        self.ldproject.add_prerequisite_to_flag(
            "release-chart", "release-new-ui", 2, "production"
        )
        self.ldproject.add_prerequisite_to_flag(
            "release-chart", "release-new-ui", 2, "test"
        )
        # # Pipeline 1 flags
        # print("  - Pipeline: Chart v2 UI")
        # self.flag_pipe_chart_v2_ui()
        # print("  - Pipeline: Chart v2 Algorithm")
        # self.flag_pipe_chart_v2_algorithm()
        # print("  - Pipeline: Chart v2 Mapping")
        # self.flag_pipe_chart_v2_mapping()
        # print("  - Pipeline: Chart v2 Data Source")
        # self.flag_pipe_chart_v2_data()
        # print("  - Pipeline: Chart v2 Libraries")
        # self.flag_pipe_chart_v2_libs()
        # # Pipeline 2 flags
        # print("  - Pipeline: DDOS Protection")
        # self.flag_pipe_ddos_protection()
        # print("  - Pipeline: Debug Logging")
        # self.flag_pipe_debug_logging()
        # print("  - Pipeline: CSPs for Website")
        # self.flag_pipe_csps_website()
        # # Release 2
        # print("  - Release: Profile - Main")
        # self.flag_rel_profile_main()
        # print("  - Release: Profile - Sales")
        # self.flag_rel_profile_sales()
        # print("  - Release: Profile - Roles")
        # self.flag_rel_profile_roles()
        # print("  - Release: Profile - Stats")
        # self.flag_rel_profile_stats()
        # # Entitlements
        # print("  - Entitlement: Status Level")
        # self.flag_ent_status_level()
        # # Experiment
        # print("  - Experiment: Feature Change")
        # self.flag_exp_feature_change()
        print("Done")
        self.flags_created = True

    def create_segments(self):
        print("Creating segments:")
        print("  - Platinum Users")
        self.segment_platinum_users()
        print("  - Gold Users")
        self.segment_gold_users()
        print("  - Silver User")
        self.segment_silver_users()
        print("  - Beta Users")
        self.segment_beta_users()
        print("  - 2FA Users")
        self.segment_2fa_users()
        print("  - Developers")
        self.segment_developers()
        print("  - QA")
        self.segment_qa()
        print("Done")
        self.segments_created = True

    def create_contexts(self):
        print("Creating contexts:")
        print("  - Audience")
        self.context_audience()
        print("  - Location")
        self.context_location()
        print("  - Device")
        self.context_device()
        print("Done")
        self.contexts_created = True

    def create_metrics(self):
        if not self.flags_created:
            print("Error: Flags not created")
            return
        print("Creating metrics:")
        print("  - AI Chatbot Positive Feedback")
        self.metric_chatbot_positive()
        print("  - AI Chatbot Negative Feedback")
        self.metric_chatbot_negative()
        print("  - Website Latency Rate")
        self.metric_latency()
        print("  - Website Error Rate")
        self.metric_error_rate()
        print("Done")
        self.metrics_created = True

    def run_experiment(self):
        # if not self.metric_groups_created:
        #     print("Error: Metric groups not created")
        #     return
        print("Creating experiment:")
        self.ldproject.toggle_flag(
            "config-ai-model",
            "on",
            "production",
            "Turn on flag for experiment",
        )
        print("  - AI Chatbot Experiment")
        self.exp_release_chatbot()
        self.ldproject.start_exp_iteration("ai-chatbot-experiment", "production")
        print("Done")
        self.experiment_created = True

    # def setup_release_pipeline(self):
    #     print("Creating release pipeline", end="...")
    #     self.rp_chart_v2_releases()
    #     print("Done")
    #     print("Adding flags to the release pipeline")
    #     print("  - Pipeline: Chart v2 UI")
    #     self.rp_flag_pipe_chart_v2_ui()
    #     print("  - Pipeline: Chart v2 Algorithm")
    #     self.rp_flag_pipe_chart_v2_algorithm()
    #     print("  - Pipeline: Chart v2 Mapping")
    #     self.rp_flag_pipe_chart_v2_mapping()
    #     print("  - Pipeline: Chart v2 Data Source")
    #     self.rp_flag_pipe_chart_v2_data()
    #     print("  - Pipeline: Chart v2 Libraries")
    #     self.rp_flag_pipe_chart_v2_libs()
    #     print("Done")

    def update_add_userid_to_flags(self):
        print("Adding maintainerId to flags", end="...")
        self.add_userid_to_flags()
        print("Done")

    def project_settings(self):
        print("Updating project settings:")
        print("  - Toggling flags")
        self.toggle_flags()
        print("  - Add targeting")
        self.add_targeting_rules()
        print("Done")

    ##################################################
    # Flag Definitions
    # ----------------
    # Each flag is defined in its own function below
    ##################################################

    ##################################################
    # AI Flag Definitions
    ##################################################
    def flag_config_system_prompt(self):
        # Config: System Prompt
        res = self.ldproject.create_flag(
            "config-system-prompt",
            "4c - Config: System Prompt",
            [
                {
                    "value": {
                        "system": "You are an expert in a software system, explaining concepts to users in a clear and concise manner."
                    },
                    "name": "Expert",
                },
                {
                    "value": {
                        "system": "You are brand new to a software system, trying your best to answer questions being asked about that system. Respond unsurely and inaccurately, with a few interjections like um, uh, or erm.",
                    },
                    "name": "Amateur",
                },
                {
                    "value": {
                        "system": "You are an old-timey professor with the air of a merlin-esque wizard. Using pompous academic language, respond to questions about a software system in a rambling and long-winded manner.",
                    },
                    "name": "Long-winded",
                },
                {
                    "value": {
                        "system": "Answer the question about a software system as concisely as possible.",
                    },
                    "name": "Concise",
                },
                {
                    "value": {
                        "system": "Answer the question as if you're Darth Vader. Do it condescendingly.",
                    },
                    "name": "Vader",
                },
            ],
            tags=["AI"],
            on_variation=0,
        )

    def flag_config_ai_model(self):
        # Config: AI Model
        res = self.ldproject.create_flag(
            "config-ai-model",
            "4b - Config: AI Model",
            [
                {
                    "value": {
                        "max_tokens": 500,
                        "modelId": "gpt-3.5-turbo",
                        "temperature": 1,
                        "top_p": 0.999,
                    },
                    "name": "OpenAI GPT-3.5 Turbo",
                    "description": "Configurations for OpenAI GPT-3.5 Turbo",
                },
                {
                    "value": {
                        "max_tokens": 500,
                        "modelId": "gpt-3.5-turbo-16k",
                        "temperature": 1,
                        "top_p": 0.999,
                    },
                    "name": "gpt-3.5-turbo-16k",
                    "description": "Configurations for OpenAI GPT-3.5-Turbo-16k",
                },
                {
                    "value": {
                        "max_tokens": 500,
                        "modelId": "gpt-4",
                        "temperature": 1,
                        "top_p": 0.999,
                    },
                    "name": "gpt-4",
                    "description": "Configurations for OpenAI GPT-4",
                },
                {
                    "value": {
                        "max_tokens": 500,
                        "modelId": "gpt-4o",
                        "temperature": 1,
                        "top_p": 0.999,
                    },
                    "name": "gpt-4o",
                },
            ],
            tags=["AI"],
        )

    ##################################################
    # Release Flag Definitions
    ##################################################

    def flag_rel_new_ui(self):
        # Release: New UI
        res = self.ldproject.create_flag(
            "release-new-ui",
            "1d - Release: New UI",
            [
                {"value": "old-ui-2000s", "name": "Old UI 2000s"},
                {"value": "old-ui-caveman", "name": "Old UI Caveman"},
                {"value": "new-ui", "name": "New UI"},
            ],
            off_variation=0,
            on_variation=2,
        )

    def flag_rel_dark_mode(self):
        # Release: Dark Mode
        varids = self.ldproject.get_flag_variations("release-new-ui")
        res = self.ldproject.create_flag(
            "dark-mode",
            "1b - Release: Dark Mode",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            prerequisites=[{"key": "release-new-ui", "variationId": varids[2]}],
        )

    def flag_rel_new_background(self):
        # Release: New Background
        varids = self.ldproject.get_flag_variations("release-new-ui")
        res = self.ldproject.create_flag(
            "new-background",
            "1a - Release: New Background",
            [
                {"value": True, "name": "Enable New Background"},
                {"value": False, "name": "Disable New Background"},
            ],
            prerequisites=[{"key": "release-new-ui", "variationId": varids[2]}],
        )

    def flag_rel_fire_overlay(self):
        # Release: Fire Overlay
        varids = self.ldproject.get_flag_variations("release-new-ui")
        res = self.ldproject.create_flag(
            "release-fire-overlay",
            "1c - Release: Fire Overlay",
            [
                {"value": True, "name": "Release Fire"},
                {"value": False, "name": "Revert Fire"},
            ],
            prerequisites=[{"key": "release-new-ui", "variationId": varids[2]}],
        )

    def flag_rel_chart(self):
        # Release: Chart
        res = self.ldproject.create_flag(
            "release-chart",
            "3 - Release: Chart",
            [
                {"value": True, "name": "Release Chart"},
                {"value": False, "name": "Hide Chart"},
            ],
            on_variation=1,
        )

    def flag_rel_chatbot(self):
        # Release: Chatbot
        res = self.ldproject.create_flag(
            "release-chatbot",
            "4a - Release: Chatbot",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            on_variation=1,
        )

    def flag_rel_gold_button(self):
        # Release: Upgrade Gold Tier Button
        res = self.ldproject.create_flag(
            "release-upgrade-gold-tier-button",
            "2 - Release: Upgrade Gold Tier Button",
            [
                {"value": True, "name": "Release Upgrade Gold Tier Button"},
                {"value": False, "name": "Hide Upgrade Gold Tier Button Unavailable"},
            ],
            on_variation=1,
        )

    ##################################################
    # Pipeline Flag Definitions
    ##################################################

    def flag_pipe_chart_v2_ui(self):
        # Pipeline: Chart v2 UI
        res = self.ldproject.create_flag(
            "pipeline-chart-v2-ui",
            "Pipeline: Chart v2 UI",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_pipe_chart_v2_algorithm(self):
        # Pipeline: Chart v2 Algorithm
        res = self.ldproject.create_flag(
            "pipeline-chart-v2-algorithm",
            "Pipeline: Chart v2 Algorithm",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_pipe_chart_v2_mapping(self):
        # Pipeline: Chart v2 Mapping
        res = self.ldproject.create_flag(
            "pipeline-chart-v2-mapping",
            "Pipeline: Chart v2 Mapping",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_pipe_chart_v2_data(self):
        # Pipeline: Chart v2 Data Source
        res = self.ldproject.create_flag(
            "pipeline-chart-v2-data",
            "Pipeline: Chart v2 Data Source",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_pipe_chart_v2_libs(self):
        # Pipeline: Chart v2 Libraries
        res = self.ldproject.create_flag(
            "pipeline-chart-v2-libs",
            "Pipeline: Chart v2 Libraries",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_pipe_ddos_protection(self):
        # Pipeline: DDOS Protection
        res = self.ldproject.create_flag(
            "pipeline-ddos-protection",
            "Pipeline: DDOS Protection",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_pipe_debug_logging(self):
        # Pipeline: Debug Logging
        res = self.ldproject.create_flag(
            "pipeline-debug-logging",
            "Pipeline: Debug Logging",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_pipe_csps_website(self):
        # Pipeline: CSPs for Website
        res = self.ldproject.create_flag(
            "pipeline-csps-website",
            "Pipeline: CSPs for Website",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_rel_profile_main(self):
        # Release: Profile - Main
        res = self.ldproject.create_flag(
            "release-profile-main",
            "Release: Profile - Main",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_rel_profile_sales(self):
        # Release: Profile - Sales
        varids = self.ldproject.get_flag_variations("release-profile-main")
        res = self.ldproject.create_flag(
            "release-profile-sales",
            "Release: Profile - Sales",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            prerequisites=[{"key": "release-profile-main", "variationId": varids[1]}],
        )

    def flag_rel_profile_roles(self):
        # Release: Profile - Roles
        varids = self.ldproject.get_flag_variations("release-profile-main")
        res = self.ldproject.create_flag(
            "release-profile-roles",
            "Release: Profile - Roles",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            prerequisites=[{"key": "release-profile-main", "variationId": varids[1]}],
        )

    def flag_rel_profile_stats(self):
        # Release: Profile - Stats
        varids = self.ldproject.get_flag_variations("release-profile-main")
        res = self.ldproject.create_flag(
            "release-profile-stats",
            "Release: Profile - Stats",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            prerequisites=[{"key": "release-profile-main", "variationId": varids[1]}],
        )

    def flag_ent_status_level(self):
        # Entitlement: Status Level
        res = self.ldproject.create_flag(
            "entitlement-status-level",
            "Entitlement: Status Level",
            [
                {"value": "bronze", "name": "Bronze"},
                {"value": "silver", "name": "Silver"},
                {"value": "gold", "name": "Gold"},
                {"value": "platinum", "name": "Platinum"},
            ],
            on_variation=0,
        )

    def flag_exp_feature_change(self):
        # Experiment: Feature Change
        res = self.ldproject.create_flag(
            "experiment-feature-change",
            "Experiment: Feature Change",
            [
                {"value": "discount", "name": "Control - Discount"},
                {"value": "bestoffer", "name": "Treament 1 - Best Offer"},
                {"value": "upgradenow", "name": "Treatment 2 - Upgrade Now"},
            ],
            on_variation=0,
        )

    ##################################################
    # Segment Definitions
    # ------------------
    # Each segment is defined in its own function below
    ##################################################

    def segment_qa(self):
        # QA
        # Test
        res = self.ldproject.create_segment(
            "qa", "QA", "test", "Segment for developers"
        )
        res = self.ldproject.add_segment_rule(
            "qa", "test", "user", "role", "in", ["QA"]
        )
        # Production
        res = self.ldproject.create_segment(
            "qa", "QA", "production", "Segment for developers"
        )
        res = self.ldproject.add_segment_rule(
            "qa", "production", "user", "role", "in", ["QA"]
        )

    def segment_developers(self):
        # Developers
        # Test
        res = self.ldproject.create_segment(
            "developer", "Developers", "test", "Segment for developers"
        )
        res = self.ldproject.add_segment_rule(
            "developer", "test", "user", "role", "in", ["developer"]
        )
        # Production
        res = self.ldproject.create_segment(
            "developer", "Developers", "production", "Segment for developers"
        )
        res = self.ldproject.add_segment_rule(
            "developer", "production", "user", "role", "in", ["developer"]
        )

    def segment_silver_users(self):
        # Silver Users
        # Test
        res = self.ldproject.create_segment(
            "silver-users", "Silver Users", "test", "Segment for Silver Users"
        )
        res = self.ldproject.add_segment_rule(
            "silver-users", "test", "user", "tier", "in", ["Silver"]
        )
        # Production
        res = self.ldproject.create_segment(
            "silver-users", "Silver Users", "production", "Segment for Silver Users"
        )
        res = self.ldproject.add_segment_rule(
            "silver-users", "production", "user", "tier", "in", ["Silver"]
        )

    def segment_gold_users(self):
        # Gold Users
        # Test
        res = self.ldproject.create_segment(
            "gold-users", "Gold Users", "test", "Segment for Gold Users"
        )
        res = self.ldproject.add_segment_rule(
            "gold-users", "test", "user", "tier", "in", ["Gold"]
        )
        # Production
        res = self.ldproject.create_segment(
            "gold-users", "Gold Users", "production", "Segment for Gold Users"
        )
        res = self.ldproject.add_segment_rule(
            "gold-users", "production", "user", "tier", "in", ["Gold"]
        )

    def segment_platinum_users(self):
        # Gold Users
        # Test
        res = self.ldproject.create_segment(
            "platinum-users", "Platinum Users", "test", "Segment for Platinum Users"
        )
        res = self.ldproject.add_segment_rule(
            "platinum-users", "test", "user", "tier", "in", ["Platinum"]
        )
        # Production
        res = self.ldproject.create_segment(
            "platinum-users",
            "Platinum Users",
            "production",
            "Segment for Platinum Users",
        )
        res = self.ldproject.add_segment_rule(
            "platinum-users", "production", "user", "tier", "in", ["Platinum"]
        )

    def segment_2fa_users(self):
        # 2FA Users
        # Test
        res = self.ldproject.create_segment(
            "2-fa-users", "2FA Users", "test", "Segment for 2FA Users"
        )
        res = self.ldproject.add_segment_rule(
            "2-fa-users", "test", "user", "2fa", "in", [True]
        )
        # Production
        res = self.ldproject.create_segment(
            "2-fa-users", "2FA Users", "production", "Segment for 2FA Users"
        )
        res = self.ldproject.add_segment_rule(
            "2-fa-users", "production", "user", "2fa", "in", [True]
        )

    def segment_beta_users(self):
        # Beta Users
        # Test
        res = self.ldproject.create_segment(
            "beta-user", "Beta Users", "test", "Segment for beta users"
        )
        res = self.ldproject.add_segment_rule(
            "beta-user", "test", "user", "beta", "in", [True]
        )
        # Production
        res = self.ldproject.create_segment(
            "beta-user", "Beta Users", "production", "Segment for beta users"
        )
        res = self.ldproject.add_segment_rule(
            "beta-user", "production", "user", "beta", "in", [True]
        )

    ##################################################
    # Metric Definitions
    # ------------------
    # Each metric is defined in its own function below
    ##################################################

    def metric_error_rate(self):
        # Error Rate
        res = self.ldproject.create_metric(
            "error-rate",
            "Website Error Rate",
            "error-rate",
            randomization_units=["user"],
            tags=["remediate"],
        )
        self.ldproject.add_maintainer_to_metric("error-rate")

    def metric_latency(self):
        # Latency
        res = self.ldproject.create_metric(
            "latency",
            "Website Latency Rate",
            "latency",
            numeric=True,
            unit="ms",
            randomization_units=["user"],
            exclude_empty_events=True,
            tags=["remediate"],
        )
        self.ldproject.add_maintainer_to_metric("latency")

    def metric_chatbot_negative(self):
        res = self.ldproject.create_metric(
            "ai-chatbot-negative-feedback",
            "AI Chatbot Negative Feedback",
            "AI Chatbot Negative Feedback",
            "",
            "custom",
            numeric=False,
            success_criteria="LowerThanBaseline",
            randomization_units=["audience"],
            tags=["experiment"],
        )

    def metric_chatbot_positive(self):
        res = self.ldproject.create_metric(
            "ai-chatbot-positive-feedback",
            "AI Chatbot Positive Feedback",
            "AI Chatbot Positive Feedback",
            "",
            "custom",
            numeric=False,
            success_criteria="HigherThanBaseline",
            randomization_units=["audience"],
            tags=["experiment"],
        )

    ### To be deleted
    def metric_discount_clicked(self):
        # Discount Clicked
        res = self.ldproject.create_metric(
            "discount-clicked",
            "Discount Clicked",
            "discount",
            "custom",
            success_criteria="HigherThanBaseline",
        )

    def metric_bestoffer_clicked(self):
        # Best Offer Clicked
        res = self.ldproject.create_metric(
            "bestoffer-clicked",
            "Best Offer Clicked",
            "bestoffer",
            "custom",
            success_criteria="HigherThanBaseline",
        )

    def metric_upgradenow_clicked(self):
        # Upgrade Now Clicked
        res = self.ldproject.create_metric(
            "upgradenow-clicked",
            "Upgrade Now Clicked",
            "upgradenow",
            "custom",
            success_criteria="HigherThanBaseline",
        )

    ##################################################
    # Metric Group Definitions
    # ------------------------
    # Each metric group is defined in its own
    # function below
    ##################################################

    ### To be deleted
    def metgroup_upgrade_account(self):
        # Upgrade Account
        res = self.ldproject.create_metric_group(
            "upgrade-metrics-group",
            "Upgrade Metrics",
            [
                {"key": "discount-clicked", "nameInGroup": "1"},
                {
                    "key": "bestoffer-clicked",
                    "nameInGroup": "2",
                },
                {
                    "key": "upgradenow-clicked",
                    "nameInGroup": "3",
                },
            ],
        )

    ##################################################
    # Context Definitions
    # ------------------------
    # Each context is defined in its own
    # function below
    ##################################################

    def context_audience(self):
        # Audience
        res = self.ldproject.create_context("audience", for_experiment=True)

    def context_location(self):
        # Location
        res = self.ldproject.create_context("location")

    def context_device(self):
        # Device
        res = self.ldproject.create_context("device")

    ##################################################
    # Experimentation Definitions
    # ---------------------------
    # Each experiment is defined in its own
    # function below
    ##################################################

    def exp_release_chatbot(self):
        # AI Chatbot Experiment
        metrics = [
            self.ldproject.exp_metric("ai-chatbot-positive-feedback", False),
            self.ldproject.exp_metric("ai-chatbot-negative-feedback", False),
        ]
        res = self.ldproject.create_experiment(
            "ai-chatbot-experiment",
            "AI Chatbot Experiment",
            "production",
            "config-ai-model",
            "We believe that the new AI model will improve the chatbot experience.",
            metrics,
            primary_key="ai-chatbot-positive-feedback",
            randomization_unit="audience",
            custom_treatment_names=[
                "GPT-3.5 Turbo",
                "GPT-3.5 Turbo 16k",
                "GPT-4",
                "GPT-4o",
            ],
        )

    ##################################################
    # Release Pipeline Definitions
    # ----------------------------
    # Each release pipeline is defined in its own
    # function below
    ##################################################

    # Create the pipeline
    def rp_chart_v2_releases(self):
        # Chart v2 Releases
        res = self.ldproject.create_release_pipeline(
            "chart-v2-releases", "Chart v2 Releases"
        )
        self.phase_ids = self.ldproject.get_pipeline_phase_ids("chart-v2-releases")

    #
    # Add flag 1 to the pipeline
    #
    def rp_flag_pipe_chart_v2_ui(self):
        # Pipeline: Chart v2 UI
        self.ldproject.add_pipeline_flag("pipeline-chart-v2-ui", "chart-v2-releases")

    #
    # Add flag 2 to the pipeline
    #
    def rp_flag_pipe_chart_v2_algorithm(self):
        # Pipeline: Chart v2 Algorithm
        self.ldproject.add_pipeline_flag(
            "pipeline-chart-v2-algorithm", "chart-v2-releases"
        )
        if not self.phase_ids:
            self.phase_ids = self.ldproject.get_pipeline_phase_ids("chart-v2-releases")
        self.ldproject.advance_flag_phase(
            "pipeline-chart-v2-algorithm", "active", self.phase_ids["test"]
        )

    #
    # Add flag 3 to the pipeline
    #
    def rp_flag_pipe_chart_v2_mapping(self):
        # Pipeline: Chart v2 Mapping
        self.ldproject.attach_metric_to_flag(
            "pipeline-chart-v2-mapping", ["error-rate", "latency"]
        )
        self.ldproject.add_pipeline_flag(
            "pipeline-chart-v2-mapping", "chart-v2-releases"
        )
        if not self.phase_ids:
            self.phase_ids = self.ldproject.get_pipeline_phase_ids("chart-v2-releases")
        self.ldproject.advance_flag_phase(
            "pipeline-chart-v2-mapping", "active", self.phase_ids["test"]
        )
        self.ldproject.advance_flag_phase(
            "pipeline-chart-v2-mapping", "active", self.phase_ids["guard"]
        )

    #
    # Add flag 4 to the pipeline
    #
    def rp_flag_pipe_chart_v2_libs(self):
        # Pipeline: Chart v2 Libraries
        self.ldproject.add_pipeline_flag("pipeline-chart-v2-libs", "chart-v2-releases")
        self.ldproject.attach_metric_to_flag("pipeline-chart-v2-libs", ["error-rate"])
        if not self.phase_ids:
            self.phase_ids = self.ldproject.get_pipeline_phase_ids("chart-v2-releases")
        self.ldproject.advance_flag_phase(
            "pipeline-chart-v2-libs", "active", self.phase_ids["test"]
        )
        self.ldproject.advance_flag_phase(
            "pipeline-chart-v2-libs", "active", self.phase_ids["guard"]
        )

    #
    # Add flag 5 to the pipeline
    #
    def rp_flag_pipe_chart_v2_data(self):
        # Pipeline: Chart v2 Data Source
        self.ldproject.add_pipeline_flag("pipeline-chart-v2-data", "chart-v2-releases")
        self.ldproject.attach_metric_to_flag("pipeline-chart-v2-data", ["latency"])
        if not self.phase_ids:
            self.phase_ids = self.ldproject.get_pipeline_phase_ids("chart-v2-releases")
        self.ldproject.advance_flag_phase(
            "pipeline-chart-v2-data", "active", self.phase_ids["test"]
        )
        self.ldproject.advance_flag_phase(
            "pipeline-chart-v2-data", "active", self.phase_ids["guard"]
        )
        self.ldproject.advance_flag_phase(
            "pipeline-chart-v2-data", "active", self.phase_ids["ga"]
        )

    ##################################################
    # Attach Maintainer to Flags
    ##################################################

    def add_userid_to_flags(self):
        res = self.ldproject.add_maintainer_to_flag("config-system-prompt")
        res = self.ldproject.add_maintainer_to_flag("config-ai-model")
        res = self.ldproject.add_maintainer_to_flag("release-chatbot")
        res = self.ldproject.add_maintainer_to_flag("release-chart")
        res = self.ldproject.add_maintainer_to_flag("release-new-ui")
        res = self.ldproject.add_maintainer_to_flag("dark-mode")
        res = self.ldproject.add_maintainer_to_flag("new-background")
        res = self.ldproject.add_maintainer_to_flag("release-fire-overlay")
        res = self.ldproject.add_maintainer_to_flag("release-upgrade-gold-tier-button")
        # res = self.ldproject.add_maintainer_to_flag("pipeline-chart-v2-ui")
        # res = self.ldproject.add_maintainer_to_flag("pipeline-chart-v2-algorithm")
        # res = self.ldproject.add_maintainer_to_flag("pipeline-chart-v2-mapping")
        # res = self.ldproject.add_maintainer_to_flag("pipeline-chart-v2-data")
        # res = self.ldproject.add_maintainer_to_flag("pipeline-chart-v2-libs")
        # res = self.ldproject.add_maintainer_to_flag("pipeline-ddos-protection")
        # res = self.ldproject.add_maintainer_to_flag("pipeline-debug-logging")
        # res = self.ldproject.add_maintainer_to_flag("pipeline-csps-website")
        # res = self.ldproject.add_maintainer_to_flag("release-profile-main")
        # res = self.ldproject.add_maintainer_to_flag("release-profile-sales")
        # res = self.ldproject.add_maintainer_to_flag("release-profile-roles")
        # res = self.ldproject.add_maintainer_to_flag("release-profile-stats")
        # res = self.ldproject.add_maintainer_to_flag("entitlement-status-level")
        # res = self.ldproject.add_maintainer_to_flag("experiment-feature-change")

    ##################################################
    # Toggle Flags
    ##################################################

    def toggle_flags(self):
        res = self.ldproject.toggle_flag("dark-mode", "on", "production")
        res = self.ldproject.toggle_flag("new-background", "on", "production")
        res = self.ldproject.toggle_flag("release-fire-overlay", "on", "production")

        res = self.ldproject.toggle_flag("dark-mode", "on", "test")
        res = self.ldproject.toggle_flag("new-background", "on", "test")
        res = self.ldproject.toggle_flag("release-fire-overlay", "on", "test")

    ##################################################
    # Add Targeting Rules
    ##################################################

    def add_targeting_rules(self):
        res = self.ldproject.add_segment_to_flag(
            "release-upgrade-gold-tier-button", "silver-users", "production"
        )
        res = self.ldproject.add_segment_to_flag(
            "release-upgrade-gold-tier-button", "silver-users", "test"
        )
        res = self.ldproject.add_segment_to_flag(
            "release-chart", "gold-users", "production", False
        )
        res = self.ldproject.add_segment_to_flag(
            "release-chart", "gold-users", "test", False
        )
        res = self.ldproject.add_segment_to_flag(
            "release-chatbot", "platinum-users", "production"
        )
        res = self.ldproject.add_segment_to_flag(
            "release-chatbot", "platinum-users", "test"
        )
        res = self.ldproject.add_segment_to_flag(
            "dark-mode", "platinum-users", "production"
        )
        res = self.ldproject.add_segment_to_flag("dark-mode", "platinum-users", "test")

        res = self.ldproject.attach_metric_to_flag(
            "release-chart", ["error-rate", "latency"]
        )
        res = self.ldproject.attach_metric_to_flag(
            "release-fire-overlay", ["error-rate", "latency"]
        )
        # res = self.ldproject.add_guarded_rollout("release-fire-overlay", "production")

    ##################################################
    # Cleanup
    ##################################################

    def cleanup(self):
        res = self.ldproject.delete_project()
