# Importations nécessaires


def create_outreach_msg(research_material, lead:dict):
    outbound_strategist = autogen.AssistantAgent(
        name="outbound_strategist",
        system_message="You are a senior outbound strategist responsable for analyzing research material and coming up with the best cold email structure with relevant personalization points",
        llm_config={"config_list": config_list},
    )

    outbound_copywriter = autogen.AssistantAgent(
        name="outbound_copywriter",
        system_message="You are a professional AI copywriter who is writing cold emails for leads. You will write a short cold email based on the structured provided by the outbound strategist, and feedback from the reviewer; After 2 rounds of content iteration, add TERMINATE to the end of the message",
        llm_config={"config_list": config_list},
    )

    reviewer = autogen.AssistantAgent(
        name="reviewer",
        system_message="You are a world class cold email critic, you will review & critic the cold email and provide feedback to writer.After 2 rounds of content iteration, add TERMINATE to the end of the message",
        llm_config={"config_list": config_list},
    )

    user_proxy = autogen.UserProxyAgent(
        name="admin",
        system_message="A human admin. Interact with outbound strategist to discuss the structure. Actual writing needs to be approved by this admin.",
        code_execution_config=False,
        is_termination_msg=lambda x: x.get("content", "") and x.get(
            "content", "").rstrip().endswith("TERMINATE"),
        human_input_mode="TERMINATE",
    )

    groupchat = autogen.GroupChat(
        agents=[user_proxy, outbound_strategist, outbound_copywriter, reviewer],
        messages=[],
        max_round=20)
    manager = autogen.GroupChatManager(groupchat=groupchat)

    user_proxy.initiate_chat(
        manager, message=f"Write a personalized cold email to {lead}, here are the material: {research_material}")

    user_proxy.stop_reply_at_receive(manager)
    user_proxy.send(
        "Give me the cold email that just generated again, return ONLY the cold email, and add TERMINATE in the end of the message", manager)

    # return the last message the expert received
    return user_proxy.last_message()["content"]


llm_config_outbound_writing_assistant = {
    "functions": [
        {
            "name": "research",
            "description": "research about a given lead, return the research material in report format",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "lead_data": {
                            "type": "object",
                            "description": "The information about a lead",
                        }
                    },
                "required": ["lead_data"],
            },
        },
        {
            "name": "create_outreach_msg",
            "description": "Write an outreach message based on the given research material & lead information",
            "parameters": {
                    "type": "object",
                    "properties": {
                        "research_material": {
                            "type": "string",
                            "description": "research material of a given topic, including reference links when available",
                        },
                        "lead": {
                            "type": "object",
                            "description": "A dictionary containing lead data",
                        }
                    },
                "required": ["research_material", "lead"],
            },
        },
    ],
    "config_list": config_list}


outbound_writing_assistant = autogen.AssistantAgent(
    name="writing_assistant",
    system_message="You are an outbound assistant, you can use research function to collect information from a lead, and then use create_outreach_msg function to write a personalized outreach message; Reply TERMINATE when your task is done",
    llm_config=llm_config_outbound_writing_assistant,
)

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    human_input_mode="TERMINATE",
    function_map={
        "create_outreach_msg": create_outreach_msg,
        "research": research,
    }
)

#Generate Lead Data
lead_data = {
    'First Name': 'Mulenga',
    'Company Name': 'Growthcurve',
    'Website URL' : 'http://growthcurve.co',
    'LinkedIn URL': 'https://www.linkedin.com/in/mulengaagley'
}

user_proxy.initiate_chat(
    outbound_writing_assistant, message=f"create an effective outreach message for the following lead {str(lead_data)}")

