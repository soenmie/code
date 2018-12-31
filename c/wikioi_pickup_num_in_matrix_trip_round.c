#include <stdio.h>
#include <stdlib.h>
#define MIN(x, y) ((x) < (y) ? (x) : (y))
#define MAX(x, y) ((x) > (y) ? (x) : (y))
int mat[200][200];
int dp[400][200][200];
int m, n;
int dpVal(int step, int x1, int x2) {
  if (step < 0 || x1 < 0 || x2 < 0) {
    return 0;
  }
  return dp[step][x1][x2];
}
int main() {
  int i, j, x1, y1, x2, y2;
  scanf("%d%d", &m, &n);
  for (i = 0; i < m; ++i) {
    for (j = 0; j < n; ++j) {
      scanf("%d", mat[i] + j);
    }
  }
  for (i = 0; i < m + n - 1; ++i) {
    for (x1 = 0; x1 <= MIN(i, m - 1); ++x1) {
      for (x2 = 0; x2 <= MIN(i, m - 1); ++x2) {
        dp[i][x1][x2] = MAX(
            MAX(dpVal(i - 1, x1, x2), dpVal(i - 1, x1, x2 - 1)),
            MAX(dpVal(i - 1, x1 - 1, x2), dpVal(i - 1, x1 - 1, x2 - 1))) +
          mat[x1][i - x1] + mat[x2][i - x2];
        dp[i][x1][x2] -= (x1 != x2 ? 0 : mat[x1][i - x1]);
      }
    }
  }
  printf("%d", dp[m + n - 2][m - 1][m - 1]);
  return 0;
}

// vim: ts=2 sw=2 et sts=2
