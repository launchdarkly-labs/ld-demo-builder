import requests
import json
import time


class LDPlatform:
    ##################################################
    # Member variables
    ##################################################
    project_key = ""
    api_key = ""
    api_key_user = ""
    client_id = ""
    sdk_key = ""
    user_id = None

    ##################################################
    # Constructor
    ##################################################
    def __init__(self, api_key, api_key_user, email):
        self.api_key = api_key
        self.api_key_user = api_key_user
        self.user_id = self.get_user_id(email)

    def getrequest(self, method, url, json=None, headers=None):

        response = requests.request(method, url, json=json, headers=headers)

        #########################
        # Rate limiting Logic
        #########################

        if "X-Ratelimit-Route-Remaining" in response.headers:
            # Completely stolen from Tom Totenberg :)
            call_limit = 5
            delay = 5
            tries = 5
            limit_remaining = response.headers["X-Ratelimit-Route-Remaining"]

            if int(limit_remaining) <= call_limit:
                resetTime = int(response.headers["X-Ratelimit-Reset"])
                currentMilliTime = round(time.time() * 1000)
                if resetTime - currentMilliTime > 0:
                    delay = round((resetTime - currentMilliTime) // 1000)
                else:
                    delay = 0

                if delay < 1:
                    delay = 0.5

                tries -= 1
                time.sleep(delay)
                if tries == 0:
                    return "Rate limit exceeded. Please try again later."
            else:
                tries = 5

        return response

    ##################################################
    # Create a project
    ##################################################
    def create_project(self, project_key, project_name):
        self.project_key = project_key
        if self.project_exists(project_key):
            return
        payload = {"key": project_key, "name": project_name}

        response = self.getrequest(
            "POST",
            "https://app.launchdarkly.com/api/v2/projects",
            json=payload,
            headers={"Authorization": self.api_key, "Content-Type": "application/json"},
        )

        data = json.loads(response.text)
        for e in data["environments"]:
            if e["key"] == "production":
                self.client_id = e["_id"]
                self.sdk_key = e["apiKey"]

        if "message" in data:
            print("Error creating project: " + data["message"])

        # remove comment and confirm requirements
        payload = [
            {"op": "replace", "path": "/requireComments", "value": False},
            {"op": "replace", "path": "/confirmChanges", "value": False},
        ]
        self.getrequest(
            "PATCH",
            "https://app.launchdarkly.com/api/v2/projects/"
            + project_key
            + "/environments/production",
            json=payload,
            headers={
                "Authorization": self.api_key,
                "Content-Type": "application/json",
                "LD-API-Version": "beta",
            },
        )
        return response

    ##################################################
    # Delete a project
    ##################################################
    def delete_project(self):
        res = self.getrequest(
            "DELETE",
            "https://app.launchdarkly.com/api/v2/projects/" + self.project_key,
            headers={"Authorization": self.api_key},
        )

    ##################################################
    # Create a flag
    ##################################################
    def create_flag(
        self,
        flag_key,
        flag_name,
        variations=[],
        purpose=None,
        on_variation=0,
        off_variation=1,
        tags=[],
        migration_stages=0,
        prerequisites=[],
    ):
        if self.flag_exists(flag_key):
            return

        payload = {
            "key": flag_key,
            "name": flag_name,
            "clientSideAvailability": {
                "usingEnvironmentId": True,
                "usingMobileKey": True,
            },
        }

        if len(variations) > 0:
            payload["variations"] = variations

        if migration_stages > 0:
            payload["migrationSettings"] = {
                "contextKind": "user",
                "stageCount": migration_stages,
            }

        if len(prerequisites) > 0:
            payload["initialPrerequisites"] = prerequisites

        if purpose is None:
            payload["defaults"] = {
                "onVariation": on_variation,
                "offVariation": off_variation,
            }
        else:
            payload["purpose"] = purpose

        if len(tags) > 0:
            payload["tags"] = tags

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }
        response = self.getrequest(
            "POST",
            "https://app.launchdarkly.com/api/v2/flags/" + self.project_key,
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating flag: " + data["message"])
        return response

    ##################################################
    # Create a segment
    ##################################################

    def create_segment(self, segment_key, segment_name, env_key, description=""):
        if self.segment_exists(segment_key, env_key):
            return

        payload = {
            "key": segment_key,
            "name": segment_name,
            "description": description,
            "unbounded": False,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }
        response = self.getrequest(
            "POST",
            "https://app.launchdarkly.com/api/v2/segments/"
            + self.project_key
            + "/"
            + env_key,
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating segment: " + data["message"])
        return response

    ##################################################
    # Add a segment rule
    ##################################################

    def add_segment_rule(
        self, segment_key, env_key, context_kind, attribute, op, value
    ):
        payload = [
            {
                "op": "add",
                "path": "/rules/0",
                "value": {
                    "clauses": [
                        {
                            "contextKind": context_kind,
                            "op": op,
                            "attribute": attribute,
                            "values": value,
                            "negate": False,
                        }
                    ],
                    "rolloutContextKind": "user",
                    "description": "",
                },
            },
        ]

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }
        response = self.getrequest(
            "PATCH",
            "https://app.launchdarkly.com/api/v2/segments/"
            + self.project_key
            + "/"
            + env_key
            + "/"
            + segment_key,
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating segment: " + data["message"])
        return response

    ##################################################
    # Create a metric
    ##################################################
    def create_metric(
        self,
        metric_key,
        metric_name,
        event_key,
        metric_description="",
        kind="custom",
        numeric=False,
        success_criteria="LowerThanBaseline",
        unit="",
        exclude_empty_events=False,
        randomization_units=[],
        tags=[],
    ):
        if self.metric_exists(metric_key):
            return

        payload = {
            "key": metric_key,
            "name": metric_name,
            "description": metric_description,
            "eventKey": event_key,
            "kind": kind,
            "maintainerId": self.user_id,
            "isNumeric": numeric,
            "successCriteria": success_criteria,
            "eventDefault": {"disabled": exclude_empty_events},
        }

        if len(tags) > 0:
            payload["tags"] = tags

        if numeric:
            payload["unit"] = unit

        if randomization_units:
            payload["randomizationUnits"] = randomization_units

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }
        response = self.getrequest(
            "POST",
            "https://app.launchdarkly.com/api/v2/metrics/" + self.project_key,
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating metric: " + data["message"])
        return response

    ##################################################
    # Create a metric group
    ##################################################
    def create_metric_group(
        self, group_key, group_name, metrics, kind="funnel", description=""
    ):
        if self.metric_group_exists(group_key):
            return

        payload = {
            "key": group_key,
            "name": group_name,
            "description": description,
            "kind": kind,
            "maintainerId": self.user_id,
            "tags": ["coast"],
            "metrics": metrics,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
            "LD-API-Version": "beta",
        }
        response = self.getrequest(
            "POST",
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/metric-groups",
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating metric group: " + data["message"])
        return response

    ##################################################
    # Create context kind
    ##################################################
    def create_context(self, context_key, for_experiment=False):
        payload = {
            "name": context_key,
            "hideInTargeting": False,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
        }
        response = self.getrequest(
            "PUT",
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/context-kinds/"
            + context_key,
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating context: " + data["message"])

        if for_experiment:
            settings = []
            response = self.getrequest(
                "GET",
                "https://app.launchdarkly.com/api/v2/projects/"
                + self.project_key
                + "/experimentation-settings",
                headers=headers,
            )
            data = json.loads(response.text)
            if "message" in data:
                print("Error getting experimentation settings: " + data["message"])
                return

            for ru in data["randomizationUnits"]:
                item = {
                    "randomizationUnit": ru["randomizationUnit"],
                    "standardRandomizationUnit": ru["standardRandomizationUnit"],
                    "default": ru["default"],
                }
                settings.append(item)

            settings.append(
                {
                    "randomizationUnit": context_key,
                    "standardRandomizationUnit": "user",
                    "default": False,
                }
            )

            payload = {
                "randomizationUnits": settings,
            }

            response = self.getrequest(
                "PUT",
                "https://app.launchdarkly.com/api/v2/projects/"
                + self.project_key
                + "/experimentation-settings",
                json=payload,
                headers=headers,
            )
            data = json.loads(response.text)
            if "message" in data:
                print("Error setting experimentation settings: " + data["message"])
        return response

    ##################################################
    # Create an experiment
    ##################################################
    def create_experiment(
        self,
        exp_key,
        exp_name,
        exp_env,
        flag_key,
        hypothesis,
        metrics,
        primary_key,
        attributes=None,
        randomization_unit="user",
        custom_treatment_names=None,
    ):
        if self.experiment_exists(exp_key, exp_env):
            return

        treatments = self.get_treatments(flag_key, custom_treatment_names)

        payload = {
            "name": exp_name,
            "key": exp_key,
            "maintainerId": self.user_id,
            "iteration": {
                "hypothesis": hypothesis,
                "canReshuffleTraffic": True,
                "metrics": metrics,
                "treatments": treatments,
                "flags": {
                    flag_key: {
                        "ruleId": "fallthrough",
                        "flagConfigVersion": 2,
                    },
                },
                "randomizationUnit": randomization_unit,
            },
        }

        if self.metric_group_exists(primary_key):
            payload["iteration"]["primaryFunnelKey"] = primary_key
        else:
            payload["iteration"]["primarySingleMetricKey"] = primary_key

        if attributes is not None:
            payload["iteration"]["attributes"] = attributes

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
            "LD-API-Version": "beta",
        }

        response = self.getrequest(
            "POST",
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/environments/"
            + exp_env
            + "/experiments",
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating experiment: " + data["message"])
        return response

    ##################################################
    # Create a release pipeline
    ##################################################
    def create_release_pipeline(self, pipeline_key, pipeline_name):
        if self.release_pipeline_exists(pipeline_key):
            return

        payload = {
            "description": "Standard pipeline to roll out to production",
            "key": pipeline_key,
            "name": pipeline_name,
            "phases": [
                {
                    "audiences": [
                        {
                            "environmentKey": "test",
                            "name": "everyone",
                            "configuration": {
                                "releaseStrategy": "immediate-rollout",
                                "requireApproval": False,
                            },
                        }
                    ],
                    "name": "Testing Phase",
                },
                {
                    "audiences": [
                        {
                            "environmentKey": "production",
                            "name": "everyone",
                            "configuration": {
                                "releaseStrategy": "monitored-release",
                                "requireApproval": False,
                                "releaseGuardianConfiguration": {
                                    "monitoringWindowMilliseconds": 3000,
                                    "rolloutWeight": 50000,
                                    "rollbackOnRegression": True,
                                },
                            },
                        }
                    ],
                    "name": "Guarded Releases",
                },
                {
                    "audiences": [
                        {
                            "environmentKey": "production",
                            "name": "everyone",
                            "configuration": {
                                "releaseStrategy": "immediate-rollout",
                                "requireApproval": False,
                            },
                        }
                    ],
                    "name": "GA",
                },
            ],
            "isProjectDefault": True,
        }

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
            "LD-API-Version": "beta",
        }
        response = self.getrequest(
            "POST",
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/release-pipelines",
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating release pipeline: " + data["message"])
        return response

    def create_shortcut(self):
        payload = {
            "name": "another",
            "key": "another",
            "icon": "bolt",
            "type": "flags",
            "context": {
                "projectKey": self.project_key,
                "environmentKeys": ["production", "test"],
                "selectedEnvironmentKey": "production",
            },
            "filters": {"filter": {"tags": ["AI"]}},
            "visibility": "me",
        }
        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key_user,
            "LD-API-Version": "beta",
        }
        response = self.getrequest(
            "POST",
            "https://app.launchdarkly.com/api/v2/shortcuts",
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating shortcut: " + data["message"])
        return response

    #####################################
    #
    # Helper functions
    #
    #####################################

    ##################################################
    # Get the User ID from the email
    ##################################################

    def get_user_id(self, email):
        if email is None:
            return None

        filter = "email:" + email
        if email == "":
            filter = "role:owner"

        res = self.getrequest(
            "GET",
            "https://app.launchdarkly.com/api/v2/members?filter=" + filter,
            headers={"Authorization": self.api_key, "Content-Type": "application/json"},
        )
        data = json.loads(res.text)
        if data["totalCount"] == 0:
            return "6320e9313293af11fa8a847f"

        self.user_id = data["items"][0]["_id"]
        return self.user_id

    ##################################################
    # Check if a project exists
    ##################################################

    def project_exists(self, project_key):
        res = self.getrequest(
            "GET",
            "https://app.launchdarkly.com/api/v2/projects/" + project_key,
            headers={"Authorization": self.api_key},
        )
        data = json.loads(res.text)
        if "message" in data:
            return False
        return True

    ##################################################
    # Check if a flag exists
    ##################################################
    def flag_exists(self, flag_key):
        res = self.getrequest(
            "GET",
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key,
            headers={"Authorization": self.api_key},
        )
        data = json.loads(res.text)
        if "message" in data:
            return False
        return True

    ##################################################
    # Check if a segment exists
    ##################################################

    def segment_exists(self, segment_key, env_key):
        res = self.getrequest(
            "GET",
            "https://app.launchdarkly.com/api/v2/segments/"
            + self.project_key
            + "/"
            + env_key
            + "/"
            + segment_key,
            headers={"Authorization": self.api_key},
        )
        if res.text.strip() == "":
            return False
        return True

    ##################################################
    # Check if a metric exists
    ##################################################
    def metric_exists(self, metric_key):
        res = self.getrequest(
            "GET",
            "https://app.launchdarkly.com/api/v2/metrics/"
            + self.project_key
            + "/"
            + metric_key,
            headers={"Authorization": self.api_key},
        )
        data = json.loads(res.text)
        if "message" in data:
            return False
        return True

    ##################################################
    # Check if a metric group exists
    ##################################################
    def metric_group_exists(self, group_key):
        res = self.getrequest(
            "GET",
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/metric-groups/"
            + group_key,
            headers={"Authorization": self.api_key, "LD-API-Version": "beta"},
        )
        data = json.loads(res.text)
        if "message" in data:
            return False
        return True

    ##################################################
    # Check if an experiment exists
    ##################################################
    def experiment_exists(self, exp_key, exp_env):
        res = self.getrequest(
            "GET",
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/environments/"
            + exp_env
            + "/experiments/"
            + exp_key,
            headers={"Authorization": self.api_key, "LD-API-Version": "beta"},
        )
        data = json.loads(res.text)
        if "message" in data:
            return False
        return True

    ##################################################
    # Check if a release pipeline exists
    ##################################################
    def release_pipeline_exists(self, pipeline_key):
        url = (
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/release-pipelines"
            + pipeline_key
        )
        res = self.getrequest(
            "GET",
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.api_key,
                "LD-API-Version": "beta",
            },
        )
        if res.status_code == 404:
            return False
        return True

    ##################################################
    # Build a treatment object
    ##################################################
    def treatment(self, name, baseline, allocation_percent, flag_key, variation_id):
        return {
            "name": name,
            "baseline": baseline,
            "allocationPercent": allocation_percent,
            "parameters": [
                {
                    "flagKey": flag_key,
                    "variationId": variation_id,
                },
            ],
        }

    #########################################################
    # Get the flag variation IDs with values, returns a list
    #########################################################
    def get_flag_variation_values(self, flag_key):
        var_ids = []

        url = (
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        res = self.getrequest("GET", url, headers=headers)
        data = json.loads(res.text)
        defaults = {
            "onVariation": data["defaults"]["onVariation"],
            "offVariation": data["defaults"]["offVariation"],
        }
        ordinal = 0
        for var in data["variations"]:
            var_ids.append(
                {"ordinal": ordinal, "value": var["value"], "id": var["_id"]}
            )
            ordinal += 1

        return var_ids, defaults

    ##################################################
    # Get the flag variation IDs, returns a list
    ##################################################
    def get_flag_variations(self, flag_key, filter=None):
        var_ids = []
        url = (
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        res = self.getrequest("GET", url, headers=headers)
        data = json.loads(res.text)
        for var in data["variations"]:
            if filter is not None:
                if var["value"] == filter:
                    var_ids.append(var["_id"])
            else:
                var_ids.append(var["_id"])
        return var_ids

    ##################################################
    # Create a list of treatments, returns a list
    ##################################################
    def get_treatments(self, flag_key, name_list=None):
        treatments = self.get_flag_variations(flag_key)
        ret_treatments = []
        names = []

        if name_list is not None:
            if len(name_list) != len(treatments):
                print("Error: name list length does not match the number of treatments")
                return
            else:
                names = name_list.copy()
        else:
            for i in range(len(treatments)):
                if i == 0:
                    names.append("Control Configuration")
                else:
                    names.append("Treatment " + str(i))
        allocs = []
        total = 0.0
        for i in range(len(treatments)):
            x = round(float(100 / len(treatments)), 2)
            allocs.append(x)
            total += x

        if total > 100.0:
            allocs[0] = float(allocs[0]) - (total - 100.0)
        if total < 100.0:
            allocs[0] = allocs[0] + (100.0 - total)

        for i in range(len(treatments)):
            is_control = False
            if i == 0:
                is_control = True
            ret_treatments.append(
                self.treatment(
                    names[i],
                    is_control,
                    allocs[i],
                    flag_key,
                    treatments[i],
                )
            )

        return ret_treatments

    ##################################################
    # Experiment metric object
    ##################################################
    def exp_metric(self, key, is_group=True):
        return {
            "key": key,
            "isGroup": is_group,
        }

    ##################################################
    # List of experiment metrics
    ##################################################
    def get_exp_metrics(self, metric_list):
        retval = []
        for m in metric_list:
            retval.append(m)

        return retval

    ##################################################
    # Add a guarded rollout to a flag
    ##################################################
    def add_guarded_rollout(
        self,
        flag_key,
        env_key,
        timeout=604800000,
        rollback=True,
        weight=50000,
        notify=True,
    ):
        vars, defaults = self.get_flag_variation_values(flag_key)

        control_var = ""
        test_var = ""

        for v in vars:
            if v["value"] == False:
                control_var = v["id"]
            else:
                test_var = v["id"]

        url = (
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key
            + "?ignoreConflicts=true"
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json; domain-model=launchdarkly.semanticpatch",
            "LD-API-Version": "beta",
        }
        payload = {
            "comment": "",
            "environmentKey": env_key,
            "instructions": [
                {
                    "kind": "updateFallthroughWithMeasuredRollout",
                    "testVariationId": test_var,
                    "controlVariationId": control_var,
                    "randomizationUnit": "user",
                    "onRegression": {"notify": notify, "rollback": rollback},
                    "onProgression": {"notify": notify, "rollForward": True},
                    "monitoringWindowMilliseconds": timeout,
                    "rolloutWeight": weight,
                }
            ],
        }
        res = self.getrequest("PATCH", url, headers=headers, json=payload)
        return res

    ##################################################
    # Toggle flag state
    ##################################################
    def toggle_flag(self, flag_key, flag_state, flag_env, comment=None):
        cmd = ""
        if flag_state == "on":
            cmd = "turnFlagOn"
        else:
            cmd = "turnFlagOff"

        url = (
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json; domain-model=launchdarkly.semanticpatch",
        }
        payload = {"environmentKey": flag_env, "instructions": [{"kind": cmd}]}
        if comment is not None:
            payload["comment"] = comment

        res = self.getrequest("PATCH", url, headers=headers, json=payload)
        return res

    ##################################################
    # Add a maintainerId to flag
    ##################################################

    def add_maintainer_to_flag(self, flag_key):
        url = (
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        payload = [
            {
                "op": "replace",
                "path": "/maintainerId",
                "value": self.user_id,
            }
        ]

        res = self.getrequest("PATCH", url, headers=headers, json=payload)
        return res

    ##################################################
    # Add a maintainerId to metric
    ##################################################

    def add_maintainer_to_metric(self, metric_key):
        url = (
            "https://app.launchdarkly.com/api/v2/metrics/"
            + self.project_key
            + "/"
            + metric_key
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
        }
        payload = [
            {
                "op": "replace",
                "path": "/maintainerId",
                "value": self.user_id,
            }
        ]

        res = self.getrequest("PATCH", url, headers=headers, json=payload)
        return res

    ##################################################
    # Add segment to flag
    ##################################################

    def add_segment_to_flag(self, flag_key, segment_key, env_key, variation=True):
        url = (
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json; domain-model=launchdarkly.semanticpatch",
        }
        var_id = self.get_flag_variations(flag_key, variation)[0]
        payload = {
            "environmentKey": env_key,
            "instructions": [
                {
                    "kind": "addRule",
                    "variationId": var_id,
                    "clauses": [
                        {
                            "contextKind": "",
                            "attribute": "segmentMatch",
                            "op": "segmentMatch",
                            "negate": False,
                            "values": [segment_key],
                        }
                    ],
                }
            ],
        }

        res = self.getrequest("PATCH", url, headers=headers, json=payload)
        return res

    ##################################################
    # Add prequisite to flag
    ##################################################

    def add_prerequisite_to_flag(self, flag_key, prerequisite_key, var_id, env_key):
        varids = self.get_flag_variations(prerequisite_key)

        url = (
            "https://app.launchdarkly.com/api/v2/flags/"
            + self.project_key
            + "/"
            + flag_key
        )
        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json; domain-model=launchdarkly.semanticpatch",
        }
        payload = {
            "environmentKey": env_key,
            "instructions": [
                {
                    "kind": "addPrerequisite",
                    "prerequisiteKey": prerequisite_key,
                    "variationId": varids[var_id],
                }
            ],
        }

        res = self.getrequest("PATCH", url, headers=headers, json=payload)
        return res

    ##################################################
    # Start experiment iteration
    ##################################################
    def start_exp_iteration(self, exp_key, exp_env):
        url = (
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/environments/"
            + exp_env
            + "/experiments/"
            + exp_key
        )

        headers = {
            "Authorization": self.api_key,
            "Content-Type": "application/json",
            "LD-API-Version": "beta",
        }
        payload = {
            "instructions": [
                {
                    "kind": "startIteration",
                    "changeJustification": "Time to start the experiment!",
                }
            ]
        }

        res = self.getrequest("PATCH", url, headers=headers, json=payload)
        return res

    ##################################################
    # Add a flag to a pipeline
    ##################################################
    def add_pipeline_flag(self, flag_key, pipeline_key):
        var_ids = self.get_flag_variations(flag_key)
        var_id = var_ids[0]
        url = (
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/flags/"
            + flag_key
            + "/release"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
            "LD-API-Version": "beta",
        }

        payload = {
            "releaseVariationId": var_id,
            "releasePipelineKey": pipeline_key,
        }

        response = requests.put(url, json=payload, headers=headers)
        return response

    ##################################################
    # Get pipeline phase IDs
    ##################################################
    def get_pipeline_phase_ids(self, pipeline_key):
        url = (
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/release-pipelines/"
            + pipeline_key
        )
        res = self.getrequest(
            "GET",
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": self.api_key,
                "LD-API-Version": "beta",
            },
        )
        data = json.loads(res.text)
        c = 0
        phases = ["test", "guard", "ga"]
        phase_ids = {}
        for p in data["phases"]:
            id = p["id"]
            phase_ids.update({phases[c]: id})
            c += 1
        return phase_ids

    ##################################################
    # Attach a metric to a flag
    ##################################################
    def attach_metric_to_flag(self, flag_key, metric_keys=[]):
        url = (
            "https://app.launchdarkly.com/api/v2/projects/"
            + self.project_key
            + "/flags/"
            + flag_key
            + "/measured-rollout-configuration"
        )

        headers = {
            "Content-Type": "application/json",
            "Authorization": self.api_key,
            "LD-API-Version": "beta",
        }

        payload = {"metricKeys": metric_keys}

        response = requests.put(url, json=payload, headers=headers)
        return response

    ##################################################
    # Advance a flag to the next phase
    ##################################################
    def advance_flag_phase(self, flag_key, status, pipeline_phase_id):
        counter = 0
        status_code = 0
        while status_code != 200:
            counter += 1
            url = (
                "https://app.launchdarkly.com/api/v2/projects/"
                + self.project_key
                + "/flags/"
                + flag_key
                + "/release/phases/"
                + pipeline_phase_id
            )

            headers = {
                "Content-Type": "application/json",
                "Authorization": self.api_key,
                "LD-API-Version": "beta",
            }

            payload = {"status": status}

            response = requests.put(url, json=payload, headers=headers)
            status_code = response.status_code
            if counter > 8:
                break
            if status_code != 200:
                data = json.loads(response.text)
                print("Error advancing flag phase: " + data["message"])
                time.sleep(2)

        return response
