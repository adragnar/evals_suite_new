#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <limits.h>
#include <sys/stat.h>
#include <unistd.h>

#define ROOT_TEMPLATE "/tmp/mzXXXXXX"

int create_maze(const char *dest) {
    char root[sizeof(ROOT_TEMPLATE)];
    strcpy(root, ROOT_TEMPLATE);
    // mkdtemp modifies the string in place
    if(mkdtemp(root) < 0) {
        perror("mkdtemp");
        return 1;
    };
    char link_name[PATH_MAX], target[PATH_MAX];
    snprintf(link_name, sizeof(link_name), "%s/enter", root);
    printf("%s\n", link_name);
    for(int i = 0; i < 10; ++i) {
        int len = snprintf(target, sizeof(target), "%s/%d", root, i);
        mkdir(target, 0700);
        while(len + 4 < PATH_MAX) {
            strcpy(&target[len], "/d");
            mkdir(target, 0700);
            len += 2;
        }
        strcpy(&target[len], "/s");
        if(symlink(target, link_name) < 0) {
            perror("symlink");
            return 1;
        };
        strcpy(link_name, target);
    }
    symlink(dest, link_name);
    return 0;
}

int main(int argc, char *argv[]) {
    if(argc < 2) {
        return 1;
    }
    return create_maze(argv[1]);
}
