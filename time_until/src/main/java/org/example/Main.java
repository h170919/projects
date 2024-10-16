package org.example;

import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Logic logic = new Logic();
        logic.daysBetween();

        Scanner scanner = new Scanner(System.in);
        while (true) {
            System.out.println("\nWhat would you like to do?\n(Press 'q' to quit, 'r' to remove a todo, or 'a' to add a todo)");
            String answer = scanner.nextLine();

            if (answer.equals("a")) {
                System.out.println("What task needs to be done?");
                String todoName = scanner.nextLine();

                System.out.println("What year does it need to be done?");
                int year = scanner.nextInt();

                System.out.println("What month does it need to get done?");
                int month = scanner.nextInt();

                System.out.println("What day does it need to get done?");
                int day = scanner.nextInt();

                scanner.nextLine();

                logic.addNewTodo(todoName, year, month, day);
            } else if (answer.equals("r")) {
                System.out.println("Which todo would you like to remove?");
                String todoToRemove = scanner.nextLine();
                logic.removeTodo(todoToRemove);
            } else if (answer.equals("q")) {
                System.out.println("Quitting the program...");
                break;
            } else {
                System.out.println("Invalid option, please try again.");
            }
        }
        scanner.close();
    }
}
