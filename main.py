import pygame
import random
import time
import math
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
ROAD_WIDTH = 300
MERGING_LANE_WIDTH = 150

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# Car dimensions
CAR_WIDTH = 40
CAR_HEIGHT = 20

class Car:
    def __init__(self, x, y, speed, color, is_merging=False):
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.is_merging = is_merging
        self.merging_initiated = False
        self.merged = False
        self.start_time = time.time()
        self.merge_time = 0
        
    def update(self, dt, cars):
        # Check for collision with cars ahead
        self.handle_collisions(cars)
        
        if self.is_merging and not self.merged:
            if not self.merging_initiated and self.x > 200:
                self.merging_initiated = True
                
            if self.merging_initiated:
                # Move diagonally to merge
                main_road_y = SCREEN_HEIGHT // 2 - ROAD_WIDTH // 4
                if self.y > main_road_y:
                    self.y -= self.speed * 0.5 * dt
                    self.x += self.speed * 0.5 * dt
                else:
                    self.merged = True
                    self.merge_time = time.time() - self.start_time
            else:
                self.x += self.speed * dt
        else:
            self.x += self.speed * dt
            
    def handle_collisions(self, cars):
        for car in cars:
            if car != self and not car.is_merging:
                # Simple collision detection for cars on the main road
                if (self.x < car.x + CAR_WIDTH and 
                    self.x + CAR_WIDTH > car.x and 
                    self.y < car.y + CAR_HEIGHT and 
                    self.y + CAR_HEIGHT > car.y):
                    self.speed = car.speed

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, CAR_WIDTH, CAR_HEIGHT))

class Simulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Traffic Merging Simulation")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 24)
        
        self.cars = []
        self.merging_cars_per_minute = 30
        self.main_road_cars_per_minute = 60
        
        self.merging_timer = 0
        self.main_road_timer = 0
        
        self.merge_times = []
        self.running = True
        
        # Stats
        self.start_time = time.time()
        self.total_cars = 0
        self.total_merging_cars = 0
        self.successful_merges = 0
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.merging_cars_per_minute += 5
                elif event.key == pygame.K_DOWN and self.merging_cars_per_minute > 5:
                    self.merging_cars_per_minute -= 5
                elif event.key == pygame.K_RIGHT:
                    self.main_road_cars_per_minute += 5
                elif event.key == pygame.K_LEFT and self.main_road_cars_per_minute > 5:
                    self.main_road_cars_per_minute -= 5
                elif event.key == pygame.K_r:
                    self.generate_report()
    
    def spawn_cars(self, dt):
        # Spawn merging cars
        self.merging_timer += dt
        if self.merging_timer >= 60 / self.merging_cars_per_minute:
            self.merging_timer = 0
            y = SCREEN_HEIGHT // 2 + ROAD_WIDTH // 4
            speed = random.uniform(60, 90)
            car = Car(0, y, speed, RED, is_merging=True)
            self.cars.append(car)
            self.total_cars += 1
            self.total_merging_cars += 1
        
        # Spawn main road cars
        self.main_road_timer += dt
        if self.main_road_timer >= 60 / self.main_road_cars_per_minute:
            self.main_road_timer = 0
            y = SCREEN_HEIGHT // 2 - ROAD_WIDTH // 4
            speed = random.uniform(80, 120)
            car = Car(0, y, speed, BLUE)
            self.cars.append(car)
            self.total_cars += 1
    
    def update(self, dt):
        # Update all cars
        for car in self.cars[:]:
            car.update(dt, self.cars)
            
            # Remove cars that have left the screen
            if car.x > SCREEN_WIDTH:
                if car.is_merging and car.merged:
                    self.successful_merges += 1
                    self.merge_times.append(car.merge_time)
                self.cars.remove(car)
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # Draw roads
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_HEIGHT // 2 - ROAD_WIDTH // 2, SCREEN_WIDTH, ROAD_WIDTH))
        
        # Draw lane markers
        for i in range(0, SCREEN_WIDTH, 40):
            pygame.draw.rect(self.screen, WHITE, (i, SCREEN_HEIGHT // 2 - 2, 20, 4))
        
        # Draw merging lane
        pygame.draw.rect(self.screen, GRAY, (0, SCREEN_HEIGHT // 2, SCREEN_WIDTH // 2, MERGING_LANE_WIDTH))
        
        # Draw all cars
        for car in self.cars:
            car.draw(self.screen)
        
        # Draw stats
        stats_text = [
            f"Merging cars per minute: {self.merging_cars_per_minute}",
            f"Main road cars per minute: {self.main_road_cars_per_minute}",
            f"Cars on screen: {len(self.cars)}",
            f"Successful merges: {self.successful_merges}"
        ]
        
        for i, text in enumerate(stats_text):
            text_surface = self.font.render(text, True, BLACK)
            self.screen.blit(text_surface, (10, 10 + i * 25))
        
        # Instructions
        controls_text = [
            "Controls:",
            "Up/Down: Adjust merging cars rate",
            "Left/Right: Adjust main road cars rate",
            "R: Generate report"
        ]
        
        for i, text in enumerate(controls_text):
            text_surface = self.font.render(text, True, BLACK)
            self.screen.blit(text_surface, (SCREEN_WIDTH - 300, 10 + i * 25))
        
        pygame.display.flip()
    
    def generate_report(self):
        run_time = time.time() - self.start_time
        
        if not self.merge_times:
            print("No merge data available yet.")
            return
        
        avg_merge_time = sum(self.merge_times) / len(self.merge_times)
        
        # Create folder for reports if it doesn't exist
        import os
        if not os.path.exists('reports'):
            os.makedirs('reports')
        
        # Generate timestamp for the report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Create plots
        plt.figure(figsize=(12, 8))
        
        # Plot 1: Merge times histogram
        plt.subplot(2, 1, 1)
        plt.hist(self.merge_times, bins=20, alpha=0.7, color='blue')
        plt.title(f'Distribution of Merge Times (Avg: {avg_merge_time:.2f}s)')
        plt.xlabel('Time (seconds)')
        plt.ylabel('Frequency')
        
        # Plot 2: Success rate vs. merging cars rate
        plt.subplot(2, 1, 2)
        success_rate = (self.successful_merges / self.total_merging_cars) * 100 if self.total_merging_cars > 0 else 0
        plt.bar(['Success Rate'], [success_rate], color='green')
        plt.title(f'Merge Success Rate: {success_rate:.1f}%')
        plt.ylabel('Percentage')
        plt.ylim(0, 100)
        
        # Add simulation parameters as text
        plt.figtext(0.5, 0.01, 
                    f"Simulation Parameters:\n"
                    f"Merging cars per minute: {self.merging_cars_per_minute}\n"
                    f"Main road cars per minute: {self.main_road_cars_per_minute}\n"
                    f"Total cars: {self.total_cars}\n"
                    f"Simulation time: {run_time:.1f} seconds", 
                    ha="center", fontsize=10, bbox={"facecolor":"orange", "alpha":0.2, "pad":5})
        
        plt.tight_layout(rect=[0, 0.05, 1, 0.95])
        
        # Save the report
        report_file = f'reports/traffic_report_{timestamp}.png'
        plt.savefig(report_file)
        plt.close()
        
        print(f"Report generated and saved to {report_file}")
    
    def run(self):
        previous_time = time.time()
        
        while self.running:
            current_time = time.time()
            dt = current_time - previous_time
            previous_time = current_time
            
            self.handle_events()
            self.spawn_cars(dt)
            self.update(dt)
            self.draw()
            
            self.clock.tick(60)
        
        pygame.quit()
        
        # Generate a final report
        self.generate_report()

if __name__ == "__main__":
    simulation = Simulation()
    simulation.run()