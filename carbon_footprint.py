from dataclasses import dataclass
from drafter import (
    route,
    Page,
    start_server,
    Button,
    TextBox,
    LineBreak,
    SelectBox,
    Header,
)
from drafter.llm import *


@dataclass
class State:
    name: str
    city: str
    us_state: str
    pounds: float
    electricity: list[str]
    water: list[str]
    transportation: list[str]
    food: list[str]


@route
def index(state: State) -> Page:
    return Page(
        state,
        [
            "Welcome to the carbon footprint generator! Fill out this brief survey to estimate your carbon footprint and receive tips to improve your lifestyle!",
            Button("Start survey", "personal_info"),
        ],
    )


@route
def personal_info(state: State) -> Page:
    return Page(
        state,
        [
            "What is your name?",
            TextBox("person"),
            LineBreak(),
            "City",
            TextBox("city"),
            "State",
            SelectBox(
                "us_state",
                [
                    "AL",
                    "AK",
                    "AZ",
                    "AR",
                    "CA",
                    "CO",
                    "CT",
                    "DE",
                    "FL",
                    "GA",
                    "HI",
                    "ID",
                    "IL",
                    "IN",
                    "IA",
                    "KS",
                    "KY",
                    "LA",
                    "ME",
                    "MD",
                    "MA",
                    "MI",
                    "MN",
                    "MS",
                    "MO",
                    "MT",
                    "NE",
                    "NV",
                    "NH",
                    "NJ",
                    "NM",
                    "NY",
                    "NC",
                    "ND",
                    "OH",
                    "OK",
                    "OR",
                    "PA",
                    "RI",
                    "SC",
                    "SD",
                    "TN",
                    "TX",
                    "UT",
                    "VT",
                    "VA",
                    "WA",
                    "WV",
                    "WI",
                    "WY",
                ],
            ),
            Button("continue", "update_personal_info"),
        ],
    )


@route
def update_personal_info(state: State, person: str, city: str, us_state: str) -> Page:
    state.name = person
    state.city = city
    state.us_state = us_state
    return electricity(state)


@route
def electricity(state: State) -> Page:
    return Page(
        state,
        [
            Header("ELECTRICITY USAGE"),
            "Do you turn the lights off when you leave the room?",
            SelectBox("lights", ["always", "mostly", "sometimes", "rarely", "never"]),
            LineBreak(),
            "What do you keep your thermostat on in the winter?",
            TextBox("winter_temp"),
            LineBreak(),
            "What do you keep your thermostat on in the summer?",
            TextBox("summer_temp"),
            LineBreak(),
            "Do you try to minimize your use of electronics? (TVs, speakers, etc.)",
            SelectBox(
                "minimize_elec", ["always", "mostly", "sometimes", "rarely", "never"]
            ),
            LineBreak(),
            "Do you use LLMs such as Gemini, ChatGPT, and others?",
            SelectBox("LLMs", ["always", "mostly", "sometimes", "rarely", "never"]),
            LineBreak(),
            "What is your home's source of electricity? (fossil fuels, nuclear, solar, geothermal, etc.)",
            TextBox("energy"),
            Button("continue", "update_electricity"),
        ],
    )


@route
def update_electricity(
    state: State,
    lights: str,
    winter_temp: str,
    summer_temp: str,
    minimize_elec: str,
    LLMs: str,
    energy: str,
) -> Page:
    state.electricity.append(lights)
    state.electricity.append(winter_temp)
    state.electricity.append(summer_temp)
    state.electricity.append(minimize_elec)
    state.electricity.append(LLMs)
    state.electricity.append(energy)
    return water(state)


@route
def water(state: State) -> Page:
    return Page(
        state,
        [
            Header("WATER USAGE"),
            "How long is your average shower (in minutes)?",
            TextBox("shower"),
            LineBreak(),
            "How often do you do full loads of laundry?",
            SelectBox("laundry", ["always", "mostly", "sometimes", "rarely", "never"]),
            LineBreak(),
            "How often do you do full dishwasher loads?",
            SelectBox(
                "dishwasher", ["always", "mostly", "sometimes", "rarely", "never"]
            ),
            "How often do you turn off faucets when not needed?",
            SelectBox("faucets", ["always", "mostly", "sometimes", "rarely", "never"]),
            Button("continue", "update_water"),
        ],
    )


@route
def update_water(
    state: State, shower: str, laundry: str, dishwasher: str, faucets: str
) -> Page:
    state.water.append(shower)
    state.water.append(laundry)
    state.water.append(dishwasher)
    state.water.append(faucets)
    return travel(state)


@route
def travel(state: State) -> Page:
    return Page(
        state,
        [
            Header("TRAVEL"),
            "What is your main mode of transportation?",
            SelectBox("transport", ["car", "public transportation", "bike", "walk"]),
            LineBreak(),
            "How often do you go on airplane trips?",
            TextBox("plane"),
            "What kind of car do you drive? (write none if you don't drive)",
            TextBox("car_type"),
            "How far do you drive on a normal day? (miles)",
            TextBox("miles"),
            Button("continue", "update_travel"),
        ],
    )


@route
def update_travel(
    state: State, transport: str, plane: str, car_type: str, miles: str
) -> Page:
    state.transportation.append(transport)
    state.transportation.append(plane)
    state.transportation.append(car_type)
    state.transportation.append(miles)
    return eating(state)


@route
def eating(state: State) -> Page:
    return Page(
        state,
        [
            "How often do you eat red meat?",
            SelectBox("red_meat", ["always", "mostly", "sometimes", "rarely", "never"]),
            "How often do you eat white meat?",
            SelectBox(
                "white_meat", ["always", "mostly", "sometimes", "rarely", "never"]
            ),
            "How often do you eat dairy products?",
            SelectBox("dairy", ["always", "mostly", "sometimes", "rarely", "never"]),
            "How much food do you typically throw away after a meal?",
            SelectBox(
                "food_waste",
                ["3/4 plate", "1/2 plate", "1/4 plate", "1/8 plate", "none"],
            ),
            "How often do you find yourself throwing away expired groceries?",
            SelectBox(
                "expired",
                ["always", "mostly", "sometimes", "rarely", "never"],
            ),
        ],
    )


@route
def update_eating(
    state: State,
    red_meat: str,
    white_meat: str,
    dairy: str,
    food_waste: str,
    expired: str,
) -> Page:
    state.food.append(red_meat)
    state.food.append(white_meat)
    state.food.append(dairy)
    state.food.append(food_waste)
    state.food.append(expired)
    pass


def electricity_number(response: list[str]) -> list[float]:
    # temperature
    e_numbers = []
    light = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I "
            + response[0]
            + " turn the lights off when I leave a room? Respond with only a float.",
        )
    ]
    light = float(call_gemini(light).content)

    e_numbers.append(light)

    temp_w = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I keep my thermostat at "
            + response[1]
            + " in the summer? Respond with only float.",
        )
    ]
    temp_w = float(call_gemini(temp_w).content)
    e_numbers.append(temp_w)

    temp_s = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I keep my thermostat at "
            + response[2]
            + " in the summer? Respond with only a float.",
        )
    ]
    temp_s = float(call_gemini(temp_s).content)
    e_numbers.append(temp_s)

    electronics = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I "
            + response[3]
            + " try to minimize the use of my electronics? Respond with only a float",
        )
    ]
    electronics = float(call_gemini(electronics).content)
    e_numbers.append(electronics)

    llm = [
        LLMMessage(
            "user",
            "by how much is my carbon footprint added to in metric tonnes of CO2 per year if I "
            + response[4]
            + " use LLMs? Respond with only a float.",
        )
    ]
    llm = float(call_gemini(llm).content)
    e_numbers.append(llm)

    electricity_type = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I "
            + response[5]
            + "? Respond with only a float",
        )
    ]
    electricity_type = float(call_gemini(electricity_type).content)
    e_numbers.append(electricity_type)

    return e_numbers


def water_number(response: list[str]) -> list[float]:
    w_numbers = []
    shower = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if my average shower is "
            + response[0]
            + " minutes? Respond with only a float.",
        )
    ]
    w_numbers.append(float(call_gemini(shower).content))

    laundry = [
        LLMMessage(
            "user",
            "by how much is my carbon footprint added to in metric tonnes of CO2 per year if my loads of laundry are "
            + response[1]
            + " full? Respond with only a float.",
        )
    ]
    w_numbers.append(float(call_gemini(laundry).content))

    dishwasher = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if my loads of the dishwasher are "
            + response[2]
            + " full? Respond with only a float.",
        )
    ]
    w_numbers.append(float(call_gemini(dishwasher).content))

    faucet = [
        LLMMessage(
            "user",
            "by how much is my carbon footprint added to in metric tonnes o CO2 per year if I "
            + response[3]
            + " turn off the faucet when not needed? Respond with only a float"
            "",
        )
    ]
    w_numbers.append(float(call_gemini(faucet).content))

    return w_numbers


def transportation_number(response: list[str]) -> list[float]:
    t_numbers = []

    mode = [
        LLMMessage(
            "user",
            "by how much is my carbon footprint added to in metric tonnes of CO2 per year if my main mode of transporation is "
            + response[0]
            + " ? Respond with only a float.",
        )
    ]
    t_numbers.append(float(call_gemini(mode).content))

    plane = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I take aiplane trips "
            + response[1]
            + " ? Respond with only a float.",
        )
    ]
    t_numbers.append(float(call_gemini(plane).content))

    car = [
        LLMMessage(
            "user",
            "by how much is my carbon footprint added to in metric tonnes of CO2 per year if I drive "
            + response[2]
            + " ? Respond with only a float.",
        )
    ]
    t_numbers.append(float(call_gemini(car).content))

    miles = [
        LLMMessage(
            "user",
            "by how much is my carbon footprint added to in metric tonnes of CO2 per year if I drive "
            + response[3]
            + " miles per day? Respond with only a float.",
        )
    ]
    t_numbers.append(float(call_gemini(miles).content))

    return t_numbers


def food_number(response: list[str]) -> list[float]:
    f_numbers = []

    red = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I "
            + response[0]
            + " eat red meat? Respond with only a float.",
        )
    ]
    f_numbers.append(float(call_gemini(red).content))

    white = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I "
            + response[1]
            + " eat white meat? Respond with only a float.",
        )
    ]
    f_numbers.append(float(call_gemini(white).content))

    meals = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I typically throw away"
            + response[2]
            + " of food after each meal? Respond with only a float",
        )
    ]
    f_numbers.append(float(call_gemini(meals).content))

    groceries = [
        LLMMessage(
            "user",
            "By how much is my carbon footprint added to in metric tonnes of CO2 per year if I "
            + response[3]
            + " throw away extra food in my fridge? Respond with only a float",
        )
    ]
    f_numbers.append(float(call_gemini(groceries).content))

    return f_numbers


"""@dataclass
class State:
    name: str
    city: str
    us_state: str
    pounds: float
    electricity: list[str]
    water: list[str]
    transportation: list[str]
    food: list[str]"""


@route
def make_report(state: State) -> Page:
    e_total = sum(electricity_number(state.electricity))
    w_total = sum(water_number(state.water))
    t_total = sum(transportation_number(state.transportation))
    f_total = sum(food_number(state.food))
    total_footprint = sum(e_total) + sum(w_total) + sum(t_total) + sum(f_total)

    us_state = state.us_state
    us_state = [
        LLMMessage(
            "user",
            "what is the average carbon footprint in metric tonnes of CO2 per year of a person living in "
            + state.us_state
            + "? Respond with a float.",
        )
    ]
    us_state = float(call_gemini(us_state).content)

    return Page(
        state,
        [
            Header("Report"),
            "Your carbon footprint: " + str(total_footprint),
            "Electricity footprint: " + str(e_total),
            "Water footprint: " + str(w_total),
            "Transportation footprint: " + str(t_total),
            "Food footprint: " + str(f_total),
            "Average carbon footprint of a person living in "
            + state.us_state
            + ": "
            + str(us_state),
            "Average carbon footprint of a someone living in the US: 16",
        ],
    )


start_server(State("", "", "", 0.0, [], [], [], []))
