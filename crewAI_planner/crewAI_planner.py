"""Welcome to Reflex!."""
import reflex as rx
from crewAI_planner.agents_tasks import *
import os

class State(rx.State):
    response = ""
    thinking = False
    response_made = False

    def get_answer(self, form_data: dict[str, str, str]):
        interests: str = form_data["interests"]
        cities: str = form_data["city"]
        days: str = form_data["day"]

        self.response_made = False
        self.thinking = True

        agents = TripAgents()
        tasks = TripTasks()

        city_agent = agents.city_selection_agent()
        local_expert_agent = agents.local_agent()
        travel_agent = agents.travel_agent()

        identify_task = tasks.identify_task(
            agent=city_agent,
            cities=cities
        )
        gather_task = tasks.gather_task(
            agent=local_expert_agent,
            interests=interests
        )
        plan_task = tasks.plan_task(
            agent=travel_agent,
            days= days
        )
        
        yield
        try:
            if self.interests == "" and self.cities == "" and self.days == "":
                return rx.window_alert("Enter informations first!")
            crew = Crew(
            agents=[
                city_agent, local_expert_agent, travel_agent
            ],
            tasks=[identify_task, gather_task, plan_task],
            verbose=True
            )
            result = crew.kickoff()
            self.response = result
            self.thinking = False
            self.response_made = True
            yield
        except Exception as e:
            self.thinking = False
            yield rx.window_alert(f"Error with OPENAI Execution or not filled information {e}")

def index():
    return rx.center(
        rx.vstack(
            rx.heading("Personal Planner", font_size="1.5em"),
            rx.form(
                rx.vstack(
                    rx.input(
                        id="interests",
                        placeholder="Enter your interests..",
                        size="3",
                    ),
                    rx.input(
                        id="city",
                        placeholder="What city are you planning your trip?",
                        size="3",
                    ),
                    rx.input(
                        id="day",
                        placeholder="Enter number of days.",
                        size="3",
                    ),
                    rx.button(
                        "Plan",
                        type="submit",
                        size="3",
                    ),
                    align="stretch",
                    spacing="4",
                ),
                on_submit = State.get_answer,
            ),
            rx.divider(),
            rx.cond(
                State.thinking,
                rx.chakra.circular_progress(is_indeterminate=True),
                rx.cond(
                    State.response_made,
                    rx.text(State.response)
                ),
            ),
            width="50em",
            bg="white",
            padding="2em",
            align="center",
        ),
        width="100%",
        height="100vh",
        background="radial-gradient(circle at 22% 11%,rgba(62, 180, 137,.20),hsla(0,0%,100%,0) 19%),radial-gradient(circle at 82% 25%,rgba(33,150,243,.18),hsla(0,0%,100%,0) 35%),radial-gradient(circle at 25% 61%,rgba(250, 128, 114, .28),hsla(0,0%,100%,0) 55%)",
    )

# Create the app.
app = rx.App(
    theme=rx.theme(
        appearance="light", has_background=True, accent_color="mint"
    ),
)
app.add_page(index, title="Reflex:Planner")
