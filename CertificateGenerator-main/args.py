import os;
import sys;
import main;

if __name__ == "__main__":
    if len(sys.argv) == 1:
        with open("./assets/man.docs","r") as file:
            print(file.read());
        sys.exit();
    else:
        arg_1 = ("--name","--body","--auth","--email");
        arg_2 = ('-f','-t');
        buffer = [];
        for idx in range(1,len(sys.argv),3):
            if sys.argv[idx] in arg_1 and \
                sys.argv[idx+1] in arg_2 and \
                not sys.argv[idx+2].startswith("-"):
                    
                    if sys.argv[idx+1] == '-f':
                        if not os.path.exists(sys.argv[idx+2]):
                             raise Exception(f'File not found : \
                                             {sys.argv[idx+2]}');
                    
                    buffer.append(
                        (sys.argv[idx],
                         sys.argv[idx+1],
                         sys.argv[idx+2])
                    );

        for idx,_ in enumerate(buffer):
            if _[1] == '-f':
                 with open(_[2],"r") as file:
                    r = file.read().strip("\n");
                    buffer[idx] = (_[0],r.split('\n'));
            else:
                buffer[idx] = (_[0],_[2]);

        main.generateModifiedCeritificate(buffer);