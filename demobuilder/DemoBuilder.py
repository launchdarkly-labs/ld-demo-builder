import LDPlatform


class DemoBuilder:
    project_created = False
    flags_created = False
    metrics_created = False
    metric_groups_created = False
    experiment_created = False
    client_id = ""
    sdk_key = ""

    # Initialize DemoBuilder
    def __init__(self, api_key, project_key, project_name):
        self.api_key = api_key
        self.project_key = project_key
        self.project_name = project_name
        self.ldproject = LDPlatform.LDPlatform(api_key)
        self.ldproject.project_key = project_key

    # Create everything
    def build(self):
        self.create_project()
        self.create_flags()
        self.create_metrics()
        self.create_metric_groups()
        self.run_experiment()

    # Create the project
    def create_project(self):
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
        print("  - Release: AI Assistant")
        self.flag_rel_ai_asst()
        print("  - Config: AI Prompt")
        self.flag_config_ai_prompt()
        print("  - Config: AI Model")
        self.flag_config_ai_model()
        print("  - Config: AI Foundation Model")
        self.flag_config_ai_fm()
        print("  - Release: New Widget")
        self.flag_rel_new_widget()
        print("  - Release: Currency Exchange")
        self.flag_rel_currency_exchange()
        print("  - Release: Profile UI")
        self.flag_rel_profile_ui()
        print("  - Release: Updated Charting Algorithm")
        self.flag_rel_updated_algorithm()
        print("  - Release: API Rate Limit")
        self.flag_rel_api_rate_limit()
        print("  - Release: Debug Logging")
        self.flag_rel_debug_logging()
        print("  - Release: DDOS Protection")
        self.flag_rel_ddos_protection()
        print("  - Release: Old to New Search Table")
        self.flag_rel_migrate_table()
        print("  - Release: Force Update")
        self.flag_rel_force_update()
        print("  - Release: Broker Dashboard")
        self.flag_rel_broker_dashboard()
        print("  - Release: Advisor Insights")
        self.flag_rel_advisor_insights()
        print("  - Show: AI Model")
        self.flag_show_ai_model()
        print("Done")
        self.flags_created = True

    def create_metrics(self):
        if not self.flags_created:
            print("Error: Flags not created")
            return
        print("Creating metrics:")
        print("  - Error Rate")
        self.metric_error_rate()
        print("  - Latency")
        self.metric_latency()
        print("  - AI Analyze Clicked")
        self.metric_ai_analyze_clicked()
        print("  - Financial Advisor Contacted")
        self.metric_advisor_contacted()
        print("  - AI Response Latency")
        self.metric_ai_response_latency()
        print("  - AI Analysis Cost")
        self.metric_ai_analysis_cost()
        print("  - AI CSAT Positive")
        self.metric_ai_csat_positive()
        print("  - AI CSAT Negative")
        self.metric_ai_csat_negative()
        print("Done")
        self.metrics_created = True

    def create_metric_groups(self):
        if not self.metrics_created:
            print("Error: Metrics not created")
            return
        print("Creating metric groups:")
        print("  - AI to Advisor Conversion")
        self.metgroup_ai_to_advisor()
        print("  - AI Performance")
        self.metgroup_ai_performance()
        print("  - AI CSAT")
        self.metgroup_ai_csat()
        print("Done")
        self.metric_groups_created = True

    # def create_experiments(self):
    #     if not self.metric_groups_created:
    #         print("Error: Metric groups not created")
    #         return
    #     print("Creating experiment:")
    #     print("  - AI Analysis to Advisor")
    #     self.exp_ai_analysis_to_advisor()
    #     print("Done")
    #     self.experiment_created = True

    def run_experiment(self):
        if not self.metric_groups_created:
            print("Error: Metric groups not created")
            return
        print("Creating experiment:")
        self.ldproject.toggle_flag(
            "config-ai-model", "on", "production", "Turn on flag for experiment"
        )
        print("  - AI Analysis to Advisor")
        self.exp_ai_analysis_to_advisor()
        self.ldproject.start_exp_iteration("ai-analysis-to-advisor", "production")
        print("Done")
        self.experiment_created = True

    ##################################################
    # Flag Definitions
    # ----------------
    # Each flag is defined in its own function below
    ##################################################

    def flag_rel_ai_asst(self):
        # Release: AI Assistant
        # TODO: part of release pipeline
        # TODO: fallback variation
        res = self.ldproject.create_flag(
            "release-ai-asst",
            "Release: AI Assistant",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            tags=["AI"],
            on_variation=1,
        )

    def flag_config_ai_prompt(self):
        # Config: AI Prompt
        # TODO: Default rule is "Sample Summary Prompt"
        res = self.ldproject.create_flag(
            "config-ai-prompt",
            "Config: AI Prompt",
            [
                {
                    "value": {
                        "system": "You are a sample summary bot. Your role is to create summaries of data based on user queries. Keep this description as short as possible while still keeping clear explanations",
                        "user": "I need to understand more about my financial positions. I have {DOLLARS} in account A and {CENTS} in account B.",
                    },
                    "name": "Sample Summary Report",
                },
                {
                    "value": {
                        "system": "You are a detailed summary bot. Your role is to create detailed summaries of data based on user queries. Be extremely verbose in your explanations, covering extensive details on the topic",
                        "user": "I need to understand more about space travel.",
                    },
                    "name": "Sample Detailed Report",
                },
            ],
        )

    def flag_config_ai_model(self):
        # Config: AI Model
        # TODO: Default rule is "Sample Model Configuration"
        res = self.ldproject.create_flag(
            "config-ai-model",
            "Config: AI Model",
            [
                {
                    "value": {
                        "max_tokens": 500,
                        "modelId": "Your-Default-Model-Configuration",
                        "temperature": 1,
                        "top_k": 250,
                        "top_p": 0.999,
                    },
                    "name": "Sample Model Configuration",
                    "description": "A basic model configuration for setting defaults in a model",
                },
                {
                    "value": {
                        "max_tokens": 4096,
                        "modelId": "gpt-4o",
                        "temperature": 1,
                    },
                    "name": "OpenAI GPT-4 Omni",
                    "description": "Configurations for OpenAI GPT-4 Omni",
                },
                {
                    "value": {
                        "anthropic_version": "bedrock-2023-05-31",
                        "max_tokens": 1000,
                        "modelId": "anthropic.claude-3-haiku-20240307-v1:0",
                        "stop_sequences": ["\n\nHuman:"],
                        "top_k": 250,
                        "top_p": 0.999,
                    },
                    "name": "Sample AWS Bedrock Claude Haiku",
                    "description": "A set of sample AI model parameters for using Claude 3 Haiku in AWS Bedrock",
                },
            ],
        )

    def flag_config_ai_fm(self):
        # Config: AI Foundation Model
        # TODO: Default rule is "Claude 3 Haiku"
        res = self.ldproject.create_flag(
            "config-ai-fm",
            "Config: AI Foundation Model",
            [
                {
                    "value": {"model": "gpt-4", "name": "OpenAI"},
                    "name": "OpenAI",
                    "description": "A basic model configuration for setting defaults in a model",
                },
                {
                    "value": {
                        "model": "anthropic.claude-3-haiku-20240307-v1:0",
                        "name": "Anthropic Claude",
                    },
                    "name": "Claude 3 Haiku",
                    "description": "Basic Model Configuration for Claude 3 Haiku",
                },
            ],
        )

    def flag_rel_new_widget(self):
        # Release: New Widget
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-new-widget",
            "Release: New Widget",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            on_variation=1,
        )

    def flag_rel_currency_exchange(self):
        # Release: Currency Exchange
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-currency-exchange",
            "Release: Currency Exchange",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_rel_profile_ui(self):
        # Release: Profile UI
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-profile-ui",
            "Release: Profile UI",
            [{"value": True}, {"value": False}],
        )

    def flag_rel_updated_algorithm(self):
        # Release: Updated Charting Alorithm
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-updated-charting-algorithm",
            "Release: Updated Charting Alorithm",
            [{"value": True}, {"value": False}],
        )

    def flag_rel_api_rate_limit(self):
        # Release: API Rate Limit
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-api-rate-limit",
            "Release: API Rate Limit",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_rel_debug_logging(self):
        # Release: Debug Logging
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-debug-logging",
            "Release: Debug Logging",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_rel_ddos_protection(self):
        # Release: DDOS Protection
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-ddos-protection",
            "Release: DDOS Protection",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            on_variation=1,
        )

    def flag_rel_migrate_table(self):
        # Release: Old to New Search Table
        # TODO: Review migration attributes
        res = self.ldproject.create_flag(
            "release-old-to-new-search-table",
            "Release: Old to New Search Table",
            purpose="migration",
            migration_stages=6,
        )

    def flag_rel_force_update(self):
        # Release: Force Update
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-force-update",
            "Release: Force Update",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_rel_broker_dashboard(self):
        # Release: Broker Dashboard
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-broker-dashboard",
            "Release: Broker Dashboard",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
        )

    def flag_rel_advisor_insights(self):
        # Release: Advisor Insights
        # TODO: Part of release pipeline
        res = self.ldproject.create_flag(
            "release-advisor-insights",
            "Release: Advisor Insights",
            [{"value": True}, {"value": False}],
        )

    def flag_show_ai_model(self):
        # Show: AI Model
        res = self.ldproject.create_flag(
            "show-ai-model",
            "Show: AI Model",
            [
                {"value": True, "name": "Available"},
                {"value": False, "name": "Unavailable"},
            ],
            on_variation=1,
            tags=["AI"],
        )

    ##################################################
    # Metric Definitions
    # ------------------
    # Each metric is defined in its own function below
    ##################################################

    def metric_error_rate(self):
        # Error Rate
        res = self.ldproject.create_metric("error-rate", "Error Rate", "error-rate")

    def metric_latency(self):
        # Latency
        res = self.ldproject.create_metric(
            "latency", "Latency", "latency", numeric=True, unit="ms"
        )

    def metric_ai_analyze_clicked(self):
        # AI Analyze Clicked
        res = self.ldproject.create_metric(
            "ai-analyze-clicked",
            "AI Analyze Clicked",
            "ai-analyze-clicked",
            success_criteria="HigherThanBaseline",
        )

    def metric_advisor_contacted(self):
        # Financial Advisor Contacted
        res = self.ldproject.create_metric(
            "financial-advisor-contacted",
            "Financial Advisor Contacted",
            "financial-advisor-contacted",
            success_criteria="HigherThanBaseline",
        )

    def metric_ai_response_latency(self):
        # AI Response Latency
        res = self.ldproject.create_metric(
            "ai-response-latency",
            "AI Reponse Latency",
            "ai-response-latency",
            numeric=True,
            unit="ms",
            exclude_empty_events=True,
        )

    def metric_ai_analysis_cost(self):
        # AI Analysis Cost
        res = self.ldproject.create_metric(
            "ai-analysis-cost",
            "AI Analysis Cost",
            "ai-analysis-cost",
            numeric=True,
            unit="$",
            exclude_empty_events=True,
        )

    def metric_ai_csat_positive(self):
        # AI CSAT Positive
        res = self.ldproject.create_metric(
            "ai-csat-positive",
            "AI CSAT Positive",
            "ai-csat-positive",
            success_criteria="HigherThanBaseline",
        )

    def metric_ai_csat_negative(self):
        # AI CSAT Negative
        res = self.ldproject.create_metric(
            "ai-csat-negative",
            "AI CSAT Negative",
            "ai-csat-negative",
        )

    ##################################################
    # Metric Group Definitions
    # ------------------------
    # Each metric group is defined in its own
    # function below
    ##################################################

    def metgroup_ai_to_advisor(self):
        # AI to Advisor Conversion
        res = self.ldproject.create_metric_group(
            "ai-to-advisor-conversion",
            "AI to Advisor Conversion",
            [
                {"key": "ai-analyze-clicked", "nameInGroup": "Step 1"},
                {
                    "key": "financial-advisor-contacted",
                    "nameInGroup": "Step 2",
                },
            ],
        )

    def metgroup_ai_performance(self):
        # AI Performance
        res = self.ldproject.create_metric_group(
            "ai-performance",
            "AI Performance",
            kind="standard",
            metrics=[
                {"key": "ai-response-latency"},
                {"key": "ai-analysis-cost"},
            ],
        )

    def metgroup_ai_csat(self):
        # AI CSAT
        res = self.ldproject.create_metric_group(
            "ai-csat",
            "AI CSAT",
            kind="standard",
            metrics=[
                {"key": "ai-csat-positive"},
                {"key": "ai-csat-negative"},
            ],
        )

    ##################################################
    # Experimentation Definitions
    # ---------------------------
    # Each experiment is defined in its own
    # function below
    ##################################################

    def exp_ai_analysis_to_advisor(self):
        # AI Analysis to Advisor
        res = self.ldproject.create_experiment(
            "ai-analysis-to-advisor",
            "AI Analysis to Advisor",
            "production",
            "config-ai-model",
            "We believe that by using more up to date AI models, we will increase customer conversions to contact their advisor.",
            primary_funnel_key="ai-to-advisor-conversion",
            attributes=["plan", "beta", "metro", "net_worth"],
        )

    ##################################################
    # Cleanup
    ##################################################

    def cleanup(self):
        res = self.ldproject.delete_project()
