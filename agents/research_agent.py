# Importations nécessaires


def research(lead_data:dict):
    llm_config_research_li = {
        "functions" : [
            {
                "name": "scrape_linkedin",
                "description": "scrape the website and look for relevant information",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "linkedin_url": {
                            "type": "string",
                            "description": "The Linkedin URL to scrape",
                        }
                    },
                    "required": ["linkedin_url"],
                },
            }
        ],
        "config_list": config_list   
    }

    outbound_researcher = autogen.AssistantAgent(
        name="Outbound_researcher",
        system_message="Research the LinkedIn Profile of a potential lead and generate a detailed report; Add TERMINATE to the end of the research report;",
        llm_config=llm_config_research_li,
    )

    user_proxy = autogen.UserProxyAgent(
        name="User_proxy",
        code_execution_config={"last_n_messages": 2, "work_dir": "coding"},
        max_consecutive_auto_reply = 3,
        default_auto_reply = 'Please continue with the task',
        is_termination_msg=lambda x: x.get("content", "") and x.get(
            "content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="TERMINATE",
        function_map={
            "scrape_linkedin": scrape_linkedin
            }
    )

    user_proxy.initiate_chat(outbound_researcher, message=f"Research this lead's website and LinkedIn Profile {str(lead_data)}")

    user_proxy.stop_reply_at_receive(outbound_researcher)
    user_proxy.send(
        "Give me the research report that just generated again, return ONLY the report", outbound_researcher)

    # return the last message the expert received
    return user_proxy.last_message()["content"]


# Create the outreach creation function

