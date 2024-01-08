# p2app/engine/main.py
#
# ICS 33 Fall 2023
# Project 2: Learning to Fly
#
# An object that represents the engine of the application.
#
# This is the outermost layer of the part of the program that you'll need to build,
# which means that YOU WILL DEFINITELY NEED TO MAKE CHANGES TO THIS FILE.

from p2app.events import *
from p2app.engine.database import *



class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.engine_connection = None


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        result = self.interpret_event(event)

        yield from result


    def interpret_event(self, event):
        result = []

        if isinstance(event, QuitInitiatedEvent):
            result.append(EndApplicationEvent)

        if isinstance(event, OpenDatabaseEvent):
            if is_database(event.path()):
                self.engine_connection = event.path()
                result.append(DatabaseOpenedEvent(event.path()))

            else:
                result.append(DatabaseOpenFailedEvent)

        elif isinstance(event, CloseDatabaseEvent):
            result.append(DatabaseClosedEvent())

        elif isinstance(event, StartContinentSearchEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if statement != 'None':
                continent_data = read_db(self.engine_connection, statement, params)

                for continent in continent_data:
                    result.append(ContinentSearchResultEvent(Continent(*continent)))

            else:
                result.append(ErrorEvent('Try Again!'))

        elif isinstance(event, StartCountrySearchEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if statement != 'None':
                country_data = read_db(self.engine_connection, statement, params)

                for country in country_data:
                    result.append(CountrySearchResultEvent(Country(*country)))

            else:
                result.append(ErrorEvent('Try Again!'))


        elif isinstance(event, StartRegionSearchEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if statement != 'None':
                region_data = read_db(self.engine_connection, statement, params)

                for region in region_data:
                    result.append(RegionSearchResultEvent(Region(*region)))

            else:
                result.append(ErrorEvent('Try Again!'))


        elif isinstance(event, LoadContinentEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)
            continent_data = read_db(self.engine_connection, statement, params)

            try:
                for continent in continent_data:
                    result.append(ContinentLoadedEvent(Continent(*continent)))

            except ErrorEvent:
                result.append(ErrorEvent('Try Again!'))

        elif isinstance(event, LoadCountryEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)
            country_data = read_db(self.engine_connection, statement, params)

            try:
                for country in country_data:
                    result.append(CountryLoadedEvent(Country(*country)))

            except ErrorEvent:
                result.append(ErrorEvent('Try Again!'))

        elif isinstance(event, LoadRegionEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)
            region_data = read_db(self.engine_connection, statement, params)

            try:
                for region in region_data:
                    result.append(RegionLoadedEvent(Region(*region)))

            except ErrorEvent:
                result.append(ErrorEvent('Try Again!'))

        elif isinstance(event, SaveNewContinentEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if is_editable(self.engine_connection, statement, params):
                result.append(ContinentSavedEvent(event.continent()))
            else:
                result.append(SaveContinentFailedEvent('Continent was not saved!'))

        elif isinstance(event, SaveNewCountryEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if is_editable(self.engine_connection, statement, params):
                result.append(CountrySavedEvent(event.country()))
            else:
                result.append(SaveCountryFailedEvent('Country was not saved!'))

        elif isinstance(event, SaveNewRegionEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if is_editable(self.engine_connection, statement, params):
                result.append(RegionSavedEvent(event.region()))
            else:
                result.append(SaveRegionFailedEvent('Region was not saved!'))

        elif isinstance(event, SaveContinentEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if is_editable(self.engine_connection, statement, params):
                result.append(ContinentSavedEvent(event.continent()))
            else:
                result.append(SaveContinentFailedEvent('Edit for Continent was unsuccessful!'))

        elif isinstance(event, SaveCountryEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if is_editable(self.engine_connection, statement, params):
                result.append(CountrySavedEvent(event.country()))
            else:
                result.append(SaveCountryFailedEvent('Edit for Country was unsuccessful!'))

        elif isinstance(event, SaveRegionEvent):
            statement = self.get_statement(event)
            params = self.get_params(event)

            if is_editable(self.engine_connection, statement, params):
                result.append(RegionSavedEvent(event.region()))
            else:
                result.append(SaveRegionFailedEvent('Edit for Region was unsuccessful!'))

        return result


    def get_params(self, event) -> list:
        """Returns a list of parameters depending on the given event"""
        result = []

        if isinstance(event, StartContinentSearchEvent):
            if event.continent_code() is not None:
                result.append(event.continent_code())
            if event.name() is not None:
                result.append(event.name())

        elif isinstance(event, StartCountrySearchEvent):
            if event.country_code() is not None:
                result.append(event.country_code())
            if event.name() is not None:
                result.append(event.name())

        elif isinstance(event, StartRegionSearchEvent):
            if event.region_code() is not None:
                result.append(event.region_code())
            if event.name() is not None:
                result.append(event.name())
            if event.local_code() is not None:
                result.append(event.local_code())

        elif isinstance(event, LoadContinentEvent):
            result.append(event.continent_id())

        elif isinstance(event, LoadCountryEvent):
            result.append(event.country_id())

        elif isinstance(event, LoadRegionEvent):
            result.append(event.region_id())

        elif isinstance(event, SaveNewContinentEvent):
            for continent in event.continent():
                result.append(continent)

        elif isinstance(event, SaveNewCountryEvent):
            for country in event.country():
                result.append(country)

        elif isinstance(event, SaveNewRegionEvent):
            for region in event.region():
                result.append(region)

        elif isinstance(event, SaveContinentEvent):
            for continent in event.continent():
                result.append(continent)
            result.append((event.continent()).continent_id)

        elif isinstance(event, SaveCountryEvent):
            for country in event.country():
                result.append(country)
            result.append((event.country()).country_id)

        elif isinstance(event, SaveRegionEvent):
            for region in event.region():
                result.append(region)
            result.append((event.region()).region_id)

        return result


    def get_statement(self, event) -> str:
        result = ''

        if isinstance(event, StartContinentSearchEvent):
            statement = 'SELECT continent_id, continent_code, name FROM continent '

            if event.continent_code() is not None:
                result = statement + 'WHERE continent_code = (?)'

                if event.name() is not None:
                    result = result + 'AND name = (?)'

            elif event.name() is not None:
                result = statement + 'WHERE name = (?)'

        elif isinstance(event, StartCountrySearchEvent):
            statement = 'SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords FROM country '

            if event.country_code() is not None:
                result = statement + 'WHERE country_code = (?)'

                if event.name() is not None:
                    result = result + 'AND name = (?)'

            elif event.name() is not None:
                result = statement + 'WHERE name = (?)'


        elif isinstance(event, StartRegionSearchEvent):
            statement = 'SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords FROM region '

            if event.region_code() is not None:
                result = statement + 'WHERE region_code = (?)'

                if event.local_code() is not None:
                    result = statement + ' AND local_code = (?)'

                    if event.name() is not None:
                        result = result + 'AND name = (?)'

            elif event.local_code() is not None:
                result = statement + 'WHERE local_code = (?)'

                if event.name() is not None:
                    result = result + 'AND name = (?)'

            elif event.name() is not None:
                result = statement + 'WHERE name = (?)'

        elif isinstance(event, LoadContinentEvent):
            result = 'SELECT continent_id, continent_code, name FROM continent WHERE continent_id = (?)'

        elif isinstance(event, LoadCountryEvent):
            result = 'SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords FROM country WHERE country_id = (?) '

        elif isinstance(event, LoadRegionEvent):
            result = 'SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords FROM region WHERE region_id = (?)'

        elif isinstance(event, SaveNewContinentEvent):
            result = 'INSERT INTO continent (continent_id, continent_code, name) VALUES (?,?,?)'

        elif isinstance(event, SaveNewCountryEvent):
            result = 'INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords) VALUES (?,?,?,?,?,?)'

        elif isinstance(event, SaveNewRegionEvent):
            result = 'INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords) VALUES (?,?,?,?,?,?,?,?)'

        elif isinstance(event, SaveContinentEvent):
            result = ('UPDATE continent '
                      'SET continent_id = (?), continent_code = (?), name = (?)'
                      'WHERE continent_id = (?)')

        elif isinstance(event, SaveCountryEvent):
            result = ('UPDATE country '
                      'SET country_id = (?), country_code = (?), name = (?), continent_id =(?), wikipedia_link = (?), keywords = (?) '
                      'WHERE country_id = (?)')

        elif isinstance(event, SaveRegionEvent):
            result = ('UPDATE region '
                      'SET region_id = (?), region_code = (?), local_code =(?), name =(?), continent_id =(?), country_id = (?), wikipedia_link = (?), keywords = (?) '
                      'WHERE region_id = (?)')

        result = result + ';'
        return result
