blasting_work_construction = {
    "dataRequest": {
        "LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "WORK_AND_CONSTRUCTION_SERVICE": None,
        "PURPOSE": None,
        "DURATION_OF_WORK": [{"start": None, "end": None}],
    }
}


infrastructure_work_construction = {
    "dataRequest": {
        # "SELECT_THE_REASON": {"selectedValue": "Contructions"},
        "LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "YOUR_NAME": None,
        "NATIONALITY": None,
        "WORK_AND_CONSTRUCTION_SERVICE": None,
        "DURATION_OF_WORK": [{"start": None, "end": None}],
        "PURPOSE": None,
        "ID": None,
    }
}


custom_request = {
    "dataRequest": {
        "CLEARING_AGENCY_NAME": None,
        "CLEARING_AGENCY_LICENSE_NUMBER": None,
        "DEPARTMENT": None,
        "IQAMA_NUMBER": None,
    }
}


helicopter_permits = {
    "dataRequest": {
        "DEPARTURE_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "HELICOPTER_COMMUNICATION_NUMBER": None,
        "PILOT_CONTACT_NUMBER": None,
        "PILOT_FULL_NAME": None,
        "PILOT_ID": None,
        "PILOT_NATIONALITY": None,
        "CREW_MEMBER_FULL_NAME": None,
        "CREW_MEMBER_ID": None,
        "CREW_MEMBER_NATIONALITY": None,
        "PURPOSE": None,
    }
}

drone_permits = {
    "dataRequest": {
        "DEPARTURE_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "DRONE_NUMBER": None,
        "OPERATOR_FULL_NAME": None,
        "OPERATOR_ID": None,
        "OPERATOR_NATIONALITY": None,
        "OPERATOR_CONTACT_NUMBER": None,
        "CREW_MEMBER_FULL_NAME": None,
        "CREW_MEMBER_ID": None,
        "CREW_MEMBER_NATIONALITY": None,
        "PURPOSE": None,
    }
}


exit_reentry_visa = {"dataRequest": {"IQAMA_NUMBER": None, "IQAMA_DURATION": None}}


family_visit_visa = {
    "dataRequest": {
        "GENDER": {"selectedValue": None},
        "VISITOR_GENDER": {"selectedValue": None},
        "VISITOR_ENTRY_LEVEL": {"selectedValue": None},
        "VISITOR_RELATIONSHIP_TO_APPLICANT": {"selectedValue": None},
        "PASSPORT_NUMBER": None,
        # "DEPARTMENT": "Sport Department ",
        "IQAMA_NUMBER": None,
        # "NATIONALITY": "Saudi",
        "MOBILE_NUMBER": None,
        # "VISITOR_NAME": "Saud",
        "VISITOR_NATIONALITY": None,
        # "VISITOR_VISA_COLLECTION_POINT": {
        #     "selectedValue": "others",
        #     "otherVal": "Home Delivery",
        # },
        "NAME_AS_IN_PASSPORT": None,
    }
}


family_iqama_approval_issuance = {
    "dataRequest": {
        "EMPLOYEE_NAME": None,
        "EMPLOYEE_ID": None,
        "EMPLOYEE_IQAMA_ID": None,
    }
}

family_iqama_issuance = {
    "dataRequest": {
        "MEDICAL_CHECKUP": {"selectedValue": None},
        "MEDICAL_INSURANCE": {"selectedValue": None},
        "EMPLOYEE_NAME": None,
        "EMPLOYEE_ID": None,
        "EMPLOYEE_IQAMA_ID": None,
    }
}

tourism = {
    "dataRequest": {
        "VISIT_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "VISITOR_FULL_NAME": None,
        "VISITOR_ID": None,
        "VISITOR_NATIONALITY": None,
        # "PURPOSE": "Tourist purpose",
        "VISIT_DATE_TIME": [{"start": None, "end": None}],
    }
}




vessels_permits = {
    "dataRequest": {
        "ROUTE_DEPARTURE": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "ROUTE_ARRIVAL": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "VESSEL_NUMBER": None,
        "VESSEL_COMPANY_NAME": None,
        "CREW_FULL_NAME": None,
        "ID_NUMBER": None,
        "NATIONALITY": None,
        "CAPTAIN_FULL_NAME": None,
        "CAPTAIN_ID": None,
        "CAPTAIN_NATIONALITY": None,
        "CAPTAIN_CONTACT_NUMBER": None,
        "MARINE_AGENT_CONTACT_NUMBER": None,
        "PURPOSE": None,
    }
}

yacht_permits = {
    "dataRequest": {
        "ROUTE_DEPARTURE": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "ROUTE_ARRIVAL": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "YACHT_COMPANY_NAME": None,
        "CREW_FULL_NAME": None,
        "ID_NUMBER": None,
        "NATIONALITY": None,
        "CAPTAIN_FULL_NAME": None,
        "CAPTAIN_ID": None,
        "CAPTAIN_NATIONALITY": None,
        "CAPTAIN_CONTACT_NUMBER": None,
        "PASSENGER_FULL_NAME": None,
        "PASSENGER_ID": None,
        "PURPOSE": None,
        "YACHT_NUMBER": None,
    }
}


cruise_permits = {
    "dataRequest": {
        "ROUTE_DEPARTURE": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "ROUTE_ARRIVAL": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "CRUISE_NUMBER": None,
        "CREW_FULL_NAME": None,
        "ID_NUMBER": None,
        "NATIONALITY": None,
        "CRUISE_COMPANY_NAME": None,
        "CAPTAIN_FULL_NAME": None,
        "CAPTAIN_ID": None,
        "CAPTAIN_NATIONALITY": None,
        "CAPTAIN_CONTACT_NUMBER": None,
        "PASSENGER_FULL_NAME": None,
        "PASSENGER_ID": None,
        "PURPOSE": None,
    }
}


boat_permits = {
    "dataRequest": {
        "ROUTE_DEPARTURE": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "ROUTE_ARRIVAL": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "BOAT_COMPANY_NAME": None,
        "BOAT_NUMBER": None,
        "CREW_FULL_NAME": None,
        "ID_NUMBER": None,
        "NATIONALITY": None,
        "CAPTAIN_FULL_NAME": None,
        "CAPTAIN_ID": None,
        "CAPTAIN_NATIONALITY": None,
        "CAPTAIN_CONTACT_NUMBER": None,
        "PASSENGER_FULL_NAME": None,
        "PURPOSE": None,
        "PASSENGER_ID": None,
    }
}


steamship_permits = {
    "dataRequest": {
        "SHIP_PICKUP_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "DRIVING_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "STEAMSHIP_NUMBER": None,
        "STEAMSHIP_COMPANY_NAME": None,
        "CREW_FULL_NAME": None,
        "ID_NUMBER": None,
        "NATIONALITY": None,
        "CAPTAIN_FULL_NAME": None,
        "CAPTAIN_ID": None,
        "CAPTAIN_NATIONALITY": None,
        "CAPTAIN_CONTACT_NUMBER": None,
        "PURPOSE": None,
    }
}


submarine_permits = {
    "dataRequest": {
        "SHIP_PICKUP_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "DRIVING_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "SUBMARINE_NUMBER": None,
        "SUBMARINE_COMPANY_NAME": None,
        "CREW_FULL_NAME": None,
        "ID_NUMBER": None,
        "NATIONALITY": None,
        "CAPTAIN_FULL_NAME": None,
        "CAPTAIN_ID": None,
        "CAPTAIN_NATIONALITY": None,
        "CAPTAIN_CONTACT_NUMBER": None,
        "PURPOSE": None,
        "PICKUP_SHIP": None,
    }
}


marine_activities_permits = {
    "dataRequest": {
        "SHIP_PICKUP_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "DRIVING_LOCATION": [
            {
                "location": None,
                "region": None,
                "latitude": None,
                "longitude": None,
            }
        ],
        "MARINE_ACTIVITES_NUMBER": None,
        "MARINE_ACTIVITES_COMPANY_NAME": None,
        "CREW_FULL_NAME": None,
        "ID_NUMBER": None,
        "NATIONALITY": None,
        "CAPTAIN_FULL_NAME": None,
        "CAPTAIN_ID": None,
        "CAPTAIN_NATIONALITY": None,
        "CAPTAIN_CONTACT_NUMBER": None,
        "PURPOSE": None,
        "PICKUP_SHIP": None,
    }
}
