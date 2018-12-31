#include <stdio.h>

#define BEGIN (-1)
#define END 30

int binary_search(const int *arr, int n, int target) {
  int i = 0, j = n - 1;
  while (i <= j) {
    int mid = (i >> 1) + (j >> 1) + (i & j & 1);
    if (arr[mid] < target) {
      i = mid + 1;
    } else {
      j = mid - 1;
    }
  }
  if (i >= n || arr[i] != target) {
    return -1;
  }
  return i;

}
int main() {
  int i;
  int arr[] = { 1, 2, 4, 6, 7, 8, 12, 14, 17, 23, 27 };
  int n = sizeof(arr) / sizeof(int);
  for (i = BEGIN; i <= END; ++i) {
    int idx = binary_search((const int *) arr, n, i);
    if (idx >= 0) {
      printf("value %d with index %d\n", i, idx);
    }

  }
  return 0;
}

// vim: ts=2 sw=2 et sts=2
