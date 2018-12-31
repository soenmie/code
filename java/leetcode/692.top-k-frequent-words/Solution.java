public class Solution {
    public List<Integer> topKFrequent(int[] nums, int k) {
        HashMap<Integer, Integer> map = new HashMap<Integer, Integer>();
        TreeSet<Long> set = new TreeSet<Long>();
        List<Integer> res = new ArrayList<Integer>();
        for (int i : nums) {
            Integer count = map.get(i);
            long sign;
            if (count == null) {
                count = 0;
            } else {
                sign = count;
                sign = (sign << 32) | i;
                set.remove(sign);
            }
            ++count;
            map.put(i, count);
            sign = count;
            sign = (sign << 32) | i;
            set.add(sign);
        }
        int i = 0;
        for (long sign : set) {
            if (i >= k) {
                break;
            }
            res.add((int)(sign >> 32));
        }
        return res;
    }
}
