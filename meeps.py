import pygame

from init import database_init, PygameRenderer
from constants import Settings, StateTracker
from game_loops.main_menu import MenuController
from game_loops.shift_s.shift import ShiftController
from game_loops.tickets.ticket_management import TicketManagementController
from game_loops.tickets.ticket_creation import TicketCreationController
from game_loops.accounts.account_management import AccountManagementController
from game_loops.accounts.account_creation import AccountCreationController
from game_loops.threats.threat_management import ThreatManagementController
from game_loops.threats.threat_creation import ThreatCreationController




class MainLoop:

    def __init__(self):
        self.connect, self.cursor = database_init(Settings.DATABASE.value)
        self.pygame_renderer = PygameRenderer()
        self.manager = self.pygame_renderer.manager
        self.current_state = MenuController(self.connect, self.cursor, self.manager)

    def main_loop(self):
        running = True
        while running:
            time_delta = self.pygame_renderer.clock.tick(Settings.FPS.value) / Settings.MS_PER_SECOND.value
            events = pygame.event.get()

            game_state = self.current_state.game_loop(events)
            if game_state == StateTracker.EXIT:
                return self._exit_game()
            
            game_state_map = {
                StateTracker.MAIN_MENU: lambda: MenuController(self.connect, self.cursor, self.manager),
                StateTracker.SHIFT: lambda: ShiftController(self.connect, self.cursor, self.manager),
                StateTracker.TICKET_MANAGEMENT: lambda: TicketManagementController(self.connect, self.cursor, self.manager),
                StateTracker.TICKET_CREATION: lambda: TicketCreationController(self.connect, self.cursor, self.manager),
                StateTracker.ACCOUNT_MANAGEMENT: lambda: AccountManagementController(self.connect, self.cursor, self.manager),
                StateTracker.ACCOUNT_CREATION: lambda: AccountCreationController(self.connect, self.cursor, self.manager),
                StateTracker.THREAT_MANAGEMENT: lambda: ThreatManagementController(self.connect, self.cursor, self.manager),
                StateTracker.THREAT_CREATION: lambda: ThreatCreationController(self.connect, self.cursor, self.manager),
            }

            new_game_state = game_state_map.get(game_state)
            if new_game_state:
                self.current_state = new_game_state()

            self.pygame_renderer.ui_renderer(time_delta)

    def _exit_game(self):
        self.connect.close()
        running = False
        return running


if __name__ == "__main__":
    initialize_game = MainLoop()
    start_game = initialize_game.main_loop()