#include <stdio.h>
#include <netdb.h>

int main() {
  const char protonames[3][5] = {
    "icmp",
    "tcp",
    "udp"
  };
  int i;
  for (i = 0; i < 3; ++i) {
    struct protoent* proto;
    proto = getprotobyname(protonames[i]);
    printf("protocol name: %s\n", proto->p_name);
    printf("protocol number: %d\n", proto->p_proto);
    printf("protocol alias: %s\n", proto->p_aliases[0]);
    printf("\n");
  }
  return 0;
}

// vim: ts=2 sw=2 et sts=2
