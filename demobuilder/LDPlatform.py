import requests
import json


class LDPlatform:
    project_key = ""
    api_key = ""
    client_id = ""
    sdk_key = ""

    def __init__(self, api_key):
        self.api_key = api_key

    def getrequest(self, method, url, json=None, headers=None):

        response = requests.request(method, url, json=json, headers=headers)

        #########################
        # Rate limiting Logic
        #########################

        # Completely stolen from Tom Totenberg :)
        # call_limit = 5
        # delay = 5
        # tries = 5
        # limit_remaining = response.headers["X-Ratelimit-Route-Remaining"]

        # if int(limit_remaining) <= call_limit:
        #     resetTime = int(response.headers["X-Ratelimit-Reset"])
        #     currentMilliTime = round(time.time() * 1000)
        #     if resetTime - currentMilliTime > 0:
        #         delay = round((resetTime - currentMilliTime) // 1000)
        #     else:
        #         delay = 0

        #     if delay < 1:
        #         delay = 0.5

        #     tries -= 1
        #     time.sleep(delay)
        #     if tries == 0:
        #         return "Rate limit exceeded. Please try again later."
        # else:
        #     tries = 5

        return response

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

        # client_id = "666b5cd5e16c371081d3ff33"
        data = json.loads(response.text)
        for e in data["environments"]:
            if e["key"] == "test":
                self.client_id = e["_id"]
            if e["key"] == "production":
                self.sdk_key = e["apiKey"]

        if "message" in data:
            print("Error creating flag: " + data["message"])
        return response

    def delete_project(self):
        res = self.getrequest(
            "DELETE",
            "https://app.launchdarkly.com/api/v2/projects/" + self.project_key,
            headers={"Authorization": self.api_key},
        )

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

    def add_release(self, flag_key):
        return

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
    ):
        if self.metric_exists(metric_key):
            return

        payload = {
            "key": metric_key,
            "name": metric_name,
            "description": metric_description,
            "eventKey": event_key,
            "kind": kind,
            "isNumeric": numeric,
            "successCriteria": success_criteria,
            "eventDefault": {"disabled": exclude_empty_events},
        }

        if numeric:
            payload["unit"] = unit

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
            print("Error creating flag: " + data["message"])
        return response

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
            "maintainerId": "5f9b3b7b7f7b7d001f7b7f7b",
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
            print("Error creating flag: " + data["message"])
        return response

    def create_experiment(
        self,
        exp_key,
        exp_name,
        exp_env,
        flag_key,
        hypothesis,
        primary_funnel_key,
        attributes,
    ):
        if self.experiment_exists(exp_key, exp_env):
            return

        payload = {
            "name": exp_name,
            "key": exp_key,
            "maintainerId": "5f9b3b7b7f7b7d001f7b7f7b",
            "iteration": {
                "hypothesis": hypothesis,
                "canReshuffleTraffic": True,
                "metrics": self.get_exp_metrics(),
                "primaryFunnelKey": primary_funnel_key,
                "treatments": self.get_treatments(flag_key),
                "flags": {
                    flag_key: {
                        "ruleId": "fallthrough",
                        "flagConfigVersion": 2,
                    },
                },
                "randomizationUnit": "user",
                "attributes": attributes,
            },
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
            + "/environments/"
            + exp_env
            + "/experiments",
            json=payload,
            headers=headers,
        )
        data = json.loads(response.text)
        if "message" in data:
            print("Error creating flag: " + data["message"])
        return response

    #####################################
    # Helper functions
    #####################################

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

    def get_flag(self, flag_key):
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
            var_ids.append(var["_id"])
        return var_ids

    def get_treatments(self, flag_key):
        treatments = self.get_flag(flag_key)
        ret_treatments = []
        treament_num = 1
        ret_treatments.append(
            self.treatment("Treatment 1", True, 10, flag_key, treatments[0])
        )

        for t in treatments:
            treament_num += 1
            ret_treatments.append(
                self.treatment("Treatment " + str(treament_num), False, 30, flag_key, t)
            )

        return ret_treatments

    def exp_metric(self, key, is_group=True):
        return {
            "key": key,
            "isGroup": is_group,
        }

    def get_exp_metrics(self):
        return [
            self.exp_metric("ai-to-advisor-conversion"),
            self.exp_metric("ai-csat"),
        ]

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
