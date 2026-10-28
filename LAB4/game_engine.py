
import pygame
import random
from pathlib import Path
from .target import Target

WHITE = (255, 255, 255)
RED = (220, 60, 60)
GREEN = (70, 190, 100)
DARK = (22, 25, 34)
GREY = (175, 180, 190)
YELLOW = (245, 205, 80)


class GameEngine:
    DIFFICULTIES = {
        "Easy": {
            "round_seconds": 30,
            "base_radius": 44,
            "min_radius": 20,
            "lifespan_frames": 120,
        },
        "Medium": {
            "round_seconds": 30,
            "base_radius": 40,
            "min_radius": 12,
            "lifespan_frames": 90,
        },
        "Hard": {
            "round_seconds": 30,
            "base_radius": 34,
            "min_radius": 8,
            "lifespan_frames": 65,
        },
    }

    def __init__(self, width, height):
        self.width = width
        self.height = height

        # Initialise these before spawning the target.
        self.margin = 60
        self.hud_height = 60

        self.font = pygame.font.SysFont("Arial", 26)
        self.large_font = pygame.font.SysFont(
            "Arial", 48, bold=True
        )
        self.small_font = pygame.font.SysFont("Arial", 20)

        self.difficulty = "Medium"
        self.quit_requested = False

        self._load_sounds()
        self._reset_round()

    def _load_sounds(self):
        """Load optional sound files from the assets folder."""
        self.sounds = {}

        try:
            if not pygame.mixer.get_init():
                pygame.mixer.init()
        except pygame.error:
            return

        project_root = Path(__file__).resolve().parent.parent
        sound_files = {
            "hit": "hit.wav",
            "miss": "miss.wav",
            "timeout": "timeout.wav",
            "round_end": "round_end.wav",
        }

        for name, filename in sound_files.items():
            path = project_root / "assets" / filename
            try:
                if path.exists():
                    self.sounds[name] = pygame.mixer.Sound(
                        str(path)
                    )
            except pygame.error:
                pass

    def _play_sound(self, name):
        sound = self.sounds.get(name)
        if sound is not None:
            try:
                sound.play()
            except pygame.error:
                pass

    def _reset_round(self):
        settings = self.DIFFICULTIES[self.difficulty]

        self.round_seconds = settings["round_seconds"]
        self.time_left_frames = self.round_seconds * 60

        self.hits = 0
        self.misses = 0
        self.score = 0

        self.game_over = False
        self._game_over_logged = False
        self.target = self._spawn_target()

    def _spawn_target(self):
        settings = self.DIFFICULTIES[self.difficulty]

        min_x = min(self.margin, max(0, self.width // 2))
        max_x = max(min_x, self.width - self.margin)

        min_y = min(
            self.margin + self.hud_height,
            max(0, self.height // 2),
        )
        max_y = max(min_y, self.height - self.margin)

        x = random.randint(min_x, max_x)
        y = random.randint(min_y, max_y)

        return Target(
            x,
            y,
            base_radius=settings["base_radius"],
            min_radius=settings["min_radius"],
            lifespan_frames=settings["lifespan_frames"],
        )

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.quit_requested = True
            return

        if event.type == pygame.KEYDOWN:
            if self.game_over:
                if event.key in (pygame.K_RETURN, pygame.K_r):
                    self._reset_round()
                elif event.key == pygame.K_ESCAPE:
                    self.quit_requested = True
                elif event.key == pygame.K_1:
                    self.set_difficulty("Easy")
                elif event.key == pygame.K_2:
                    self.set_difficulty("Medium")
                elif event.key == pygame.K_3:
                    self.set_difficulty("Hard")
            return

        if event.type != pygame.MOUSEBUTTONDOWN:
            return

        if self.game_over:
            self._handle_menu_click(event.pos)
        elif event.button == 1:
            self._handle_click(event.pos)

    def _handle_menu_click(self, pos):
        x, y = pos
        center_x = self.width // 2
        center_y = self.height // 2

        option_y = center_y + 15

        options = [
            ("Easy", pygame.Rect(
                center_x - 210, option_y, 120, 48
            )),
            ("Medium", pygame.Rect(
                center_x - 60, option_y, 120, 48
            )),
            ("Hard", pygame.Rect(
                center_x + 90, option_y, 120, 48
            )),
        ]

        for name, rect in options:
            if rect.collidepoint(x, y):
                self.set_difficulty(name)
                return

        replay_rect = pygame.Rect(
            center_x - 150, center_y + 90, 140, 48
        )
        exit_rect = pygame.Rect(
            center_x + 10, center_y + 90, 140, 48
        )

        if replay_rect.collidepoint(x, y):
            self._reset_round()
        elif exit_rect.collidepoint(x, y):
            self.quit_requested = True

    def set_difficulty(self, difficulty):
        if difficulty not in self.DIFFICULTIES:
            return

        self.difficulty = difficulty
        self._reset_round()

    def _handle_click(self, pos):
        x, y = pos

        if self.target.contains_point(x, y):
            self.hits += 1
            self.score += 1
            self._play_sound("hit")
            self.target = self._spawn_target()
        else:
            self.misses += 1
            self._play_sound("miss")

    def handle_input(self):
        # Mouse and keyboard input are handled through events.
        pass

    def update(self):
        if self.game_over:
            return

        self.time_left_frames -= 1

        if self.time_left_frames <= 0:
            self.time_left_frames = 0
            self.game_over = True
            self._play_sound("round_end")

            if not self._game_over_logged:
                print(
                    f"Time's up! Final score: {self.score} "
                    f"Accuracy: {self.accuracy()}%"
                )
                self._game_over_logged = True
            return

        self.target.update()

        if self.target.expired():
            self.misses += 1
            self._play_sound("timeout")
            self.target = self._spawn_target()

    def accuracy(self):
        total = self.hits + self.misses

        if total == 0:
            return 0.0

        return round(100 * self.hits / total, 1)

    def _draw_button(
        self, screen, rect, label, fill, text_color=WHITE
    ):
        pygame.draw.rect(
            screen, fill, rect, border_radius=8
        )
        pygame.draw.rect(
            screen, WHITE, rect, width=2, border_radius=8
        )

        text = self.small_font.render(
            label, True, text_color
        )
        screen.blit(text, text.get_rect(center=rect.center))

    def render(self, screen):
        screen.fill(DARK)

        if not self.game_over:
            radius = max(
                1, int(self.target.visual_radius())
            )
            pygame.draw.circle(
                screen,
                RED,
                (self.target.x, self.target.y),
                radius,
            )
            pygame.draw.circle(
                screen,
                WHITE,
                (self.target.x, self.target.y),
                radius,
                2,
            )

        score_text = self.font.render(
            f"Score: {self.score}", True, WHITE
        )
        screen.blit(score_text, (10, 10))

        seconds_left = max(
            0, self.time_left_frames // 60
        )
        timer_text = self.font.render(
            f"Time: {seconds_left}s", True, WHITE
        )
        screen.blit(
            timer_text, (self.width - 140, 10)
        )

        accuracy_text = self.font.render(
            f"Accuracy: {self.accuracy()}%",
            True,
            WHITE,
        )
        screen.blit(
            accuracy_text,
            (self.width // 2 - 90, 10),
        )

        if self.game_over:
            self._render_game_over(screen)

    def _render_game_over(self, screen):
        overlay = pygame.Surface(
            (self.width, self.height),
            pygame.SRCALPHA,
        )
        overlay.fill((0, 0, 0, 190))
        screen.blit(overlay, (0, 0))

        center_x = self.width // 2
        center_y = self.height // 2

        title = self.large_font.render(
            "GAME OVER", True, YELLOW
        )
        screen.blit(
            title,
            title.get_rect(
                center=(center_x, center_y - 115)
            ),
        )

        score_text = self.font.render(
            f"Final score: {self.score}", True, WHITE
        )
        screen.blit(
            score_text,
            score_text.get_rect(
                center=(center_x, center_y - 60)
            ),
        )

        accuracy_text = self.font.render(
            f"Final accuracy: {self.accuracy()}%",
            True,
            WHITE,
        )
        screen.blit(
            accuracy_text,
            accuracy_text.get_rect(
                center=(center_x, center_y - 25)
            ),
        )

        option_y = center_y + 15

        self._draw_button(
            screen,
            pygame.Rect(
                center_x - 210, option_y, 120, 48
            ),
            "Easy (1)",
            GREEN if self.difficulty == "Easy" else GREY,
        )

        self._draw_button(
            screen,
            pygame.Rect(
                center_x - 60, option_y, 120, 48
            ),
            "Medium (2)",
            GREEN if self.difficulty == "Medium" else GREY,
        )

        self._draw_button(
            screen,
            pygame.Rect(
                center_x + 90, option_y, 120, 48
            ),
            "Hard (3)",
            GREEN if self.difficulty == "Hard" else GREY,
        )

        self._draw_button(
            screen,
            pygame.Rect(
                center_x - 150, center_y + 90, 140, 48
            ),
            "Replay (Enter)",
            GREEN,
        )

        self._draw_button(
            screen,
            pygame.Rect(
                center_x + 10, center_y + 90, 140, 48
            ),
            "Exit (Esc)",
            RED,
        )

        hint = self.small_font.render(
            "Choose a difficulty, replay, or exit",
            True,
            WHITE,
        )
        screen.blit(
            hint,
            hint.get_rect(
                center=(center_x, center_y + 160)
            ),
        )
