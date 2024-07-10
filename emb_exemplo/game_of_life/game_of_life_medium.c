#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define GAME_SIZE 90
#define TRUE 1
#define FALSE 0
#define TOTAL_ITERATIONS 1
#define BIRTH_THRESHOLD 89

void init_game_matrix(int game_matrix[GAME_SIZE][GAME_SIZE]) {
  srand(time(NULL));

  int i;
  for (i = 0; i < GAME_SIZE; i++) {
    int j;
    for (j = 0; j < GAME_SIZE; j++) {
      game_matrix[i][j] = FALSE;

      int random_integer = rand() % 100;

      if (random_integer >= BIRTH_THRESHOLD) {
        game_matrix[i][j] = TRUE;
      }
    }
  }
}

void print_game_matrix(int game_matrix[GAME_SIZE][GAME_SIZE]) {
  int i;
  for (i = 0; i < GAME_SIZE; i++) {
    int j;
    for (j = 0; j < GAME_SIZE; j++) {
      if (game_matrix[i][j]) {
        printf("X");
      } else {
        printf(" ");
      }
    }
    printf("\n");
  }
}

void update_game_matrix(int game_matrix[GAME_SIZE][GAME_SIZE]) {
  srand(time(NULL));
  int i;
  for (i = 0; i < GAME_SIZE; i++) {
    int j;
    for (j = 0; j < GAME_SIZE; j++) {
      int left_neighbour = FALSE;
      int right_neighbour = FALSE;
      int up_neighbour = FALSE;
      int down_neighbour = FALSE;
      int left_up_neighbour = FALSE;
      int right_up_neighbour = FALSE;
      int left_down_neighbour = FALSE;
      int right_down_neighbour = FALSE;

      if (i - 1 >= 0) {
        left_neighbour = game_matrix[i - 1][j];
      }
      if (i + 1 < GAME_SIZE) {
        right_neighbour = game_matrix[i + 1][j];
      }
      if (j - 1 >= 0) {
        down_neighbour = game_matrix[i][j - 1];
      }
      if (j + 1 < GAME_SIZE) {
        up_neighbour = game_matrix[i][j + 1];
      }

      if (i - 1 >= 0 && j - 1 >= 0) {
        left_down_neighbour = game_matrix[i - 1][j - 1];
      }
      if (i + 1 < GAME_SIZE && j - 1 >= 0) {
        right_down_neighbour = game_matrix[i + 1][j - 1];
      }
      if (i - 1 >= 0 && j + 1 < GAME_SIZE) {
        left_up_neighbour = game_matrix[i - 1][j + 1];
      }
      if (i + 1 < GAME_SIZE && j + 1 < GAME_SIZE) {
        right_up_neighbour = game_matrix[i + 1][j + 1];
      }

      int total_sum = left_neighbour + right_neighbour + up_neighbour +
                      down_neighbour + left_down_neighbour + left_up_neighbour +
                      right_down_neighbour + right_up_neighbour;

      if (game_matrix[i][j]) {
        if (total_sum < 2 || total_sum > 3) {
          game_matrix[i][j] = FALSE;
        }
      } else {
        if (total_sum >= 3) {
          game_matrix[i][j] = TRUE;
        }
      }

      int random_coord_x = rand() % GAME_SIZE;
      int random_coord_y = rand() % GAME_SIZE;
      int random_integer = rand() % 100;

      if (random_integer >= 19) {
        game_matrix[i][j] = game_matrix[random_coord_x][random_coord_y];
      }
    }
  }
}

int main() {
  int game_matrix[GAME_SIZE][GAME_SIZE];

  init_game_matrix(game_matrix);

  int _i;
  for (_i = 0; _i < TOTAL_ITERATIONS; _i++) {
    // print_game_matrix(game_matrix);
    update_game_matrix(game_matrix);
  }
}
