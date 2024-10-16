package org.example;

import com.google.gson.Gson;
import com.google.gson.JsonObject;
import com.google.gson.JsonArray;

import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDate;
import java.time.temporal.ChronoUnit;

public class Logic {

  // TODO remove the need for absolute path
  private static final String FILE_PATH = "/home/bob/Documents/GitHub/one_project_per_week/time_until/src/main/java/org/example/todos.json";

  public static void daysBetween() {
    LocalDate currentDate = LocalDate.now();
    Gson gson = new Gson();

    try (FileReader reader = new FileReader(FILE_PATH)) {
      JsonObject jsonObject = gson.fromJson(reader, JsonObject.class);

      for (String key : jsonObject.keySet()) {
        JsonArray todoArray = jsonObject.getAsJsonArray(key);

        if (todoArray == null || todoArray.size() < 3) {
          System.out.println("Invalid date array for key: " + key);
          continue;
        }

        int year = todoArray.get(0).getAsInt();
        int month = todoArray.get(1).getAsInt();
        int day = todoArray.get(2).getAsInt();

        LocalDate todoDate = LocalDate.of(year, month, day);
        Long daysBetween = ChronoUnit.DAYS.between(currentDate, todoDate);

        System.out
            .println(
                "\nDays until [" + key + "]: " + daysBetween + " days\n\t Due date: " + day + "/" + month + "/" + year);
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  public static void addNewTodo(String key, int year, int month, int day) {
    Gson gson = new Gson();

    try (FileReader reader = new FileReader(FILE_PATH)) {
      JsonObject jsonObject = gson.fromJson(reader, JsonObject.class);
      JsonArray dateArray = new JsonArray();
      dateArray.add(year);
      dateArray.add(month);
      dateArray.add(day);

      jsonObject.add(key, dateArray);

      try (FileWriter writer = new FileWriter(FILE_PATH)) {
        gson.toJson(jsonObject, writer);
      } catch (IOException e) {
        e.printStackTrace();
      }

      System.out.println("Added new todo: " + key);

    } catch (IOException e) {
      e.printStackTrace();
    }
  }

  public static void removeTodo(String key) {
    Gson gson = new Gson();

    try (FileReader reader = new FileReader(FILE_PATH)) {
      JsonObject jsonObject = gson.fromJson(reader, JsonObject.class);

      if (jsonObject.has(key)) {
        jsonObject.remove(key);
        System.out.println("Removed todo [" + key + "]");
      } else {
        System.out.println("Todo not found");
      }

      try (FileWriter writer = new FileWriter(FILE_PATH)) {
        gson.toJson(jsonObject, writer);
      }
    } catch (IOException e) {
      e.printStackTrace();
    }
  }
}
