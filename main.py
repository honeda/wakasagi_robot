from lib.servo import SG90

if __name__ == "__main__":
    servo = SG90(15)
    for _ in range(10):
        servo.go_angle(87, 75, delay=10)
        servo.go_angle(75, 87, delay=10)