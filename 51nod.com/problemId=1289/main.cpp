// https://www.51nod.com/Html/Challenge/Problem.html#problemId=1289
#include<iostream>
#include<vector>
using namespace std;
int solve(vector<int> &size, vector<int> &dir);

int main() {
    int n;
    cin >> n;
    vector<int> size(n), dir(n);
    for (int i = 0; i < n; ++i) {
        cin >> size[i];
        cin >> dir[i];
    }
    cout << solve(size, dir);
}
int solve(vector<int> &size, vector<int> &dir) {
    int ans = 0;
    vector<int> stack;
    for (int i = 0; i < dir.size(); i++) {
        if (dir[i] == 0) {
            while (!stack.empty()) {
                int top = stack.back();
                if (top > size[i]) {
                    break;
                }
                stack.pop_back();
            }
            if (stack.empty()) {
                ++ans;
            }
        }
        else {
            stack.push_back(size[i]);
        }
    }
    return ans + stack.size();
}
