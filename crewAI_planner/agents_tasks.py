import os
from langchain_openai import ChatOpenAI
from crewai_tools import SerperDevTool
from crewai import Agent, Task, Crew
from dotenv import load_dotenv

load_dotenv()

# Checking if the API key is set properly
if (not os.getenv("OPENAI_API_KEY")) and (not os.getenv("SERPER_API_KEY")):
    raise Exception("Please set OPENAI_API_KEY and serper environment variable.")

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")

search_tool = SerperDevTool()

class TripAgents():

    def city_selection_agent(self):
        return Agent(
            llm=llm,
            role="City Selection Expert",
            goal="Select the best city based on weather, season, and prices",
            backstory="An expert in analyzing travel data to pick ideal destinations",
            tools=[search_tool],
            verbose=True
        )
    
    def local_agent(self):
        return Agent(
            llm=llm,
            role="Local expert at this city",
            goal="Provide Best insights about selected city",
            backstory="A knowledgeable local guide with extensive information",
            tools=[search_tool],
            verbose=True
        )
    def travel_agent(self):
        return Agent(
            llm=llm,
            role="Amazing Travel Concierge",
            goal="Create most amazing travel itineraries with budget and packing suggestions for city",
            backstory="Specialist in traveling planning and logistic with decades of experience",
            tools=[search_tool],
            verbose=True
        )

class TripTasks():
    def identify_task(self, agent, cities):
        return Task(description=f"Analyze and select {cities} for trip based on weather patterns, seasonal events, and travel costs.",
                    expected_output="Detailed report on chosen city including attractions.",
                    agent=agent
                    )
               
    def gather_task(self, agent, interests):
        return Task(description=f"Compile an in-depth guide for someone traveling there and wanting to have BEST trip ever, interests: {interests}",
                    expected_output="comprehensive city guide tailored to enhance the travel experience",
                    agent=agent
                    )
    
    def plan_task(self, days, agent):
        return Task(description=f"Expand this guide into a full {days} day travel itinerary with detailed per-day plans",
                    expected_output="A complete expanded travel plan and suggest actual places to visit.",
                    agent=agent
                    )

