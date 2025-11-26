from Extract.convertion import tsvFileToCsv
import sys

def main():
    tsvFileToCsv(sys.argv[1])
    
if __name__ == "__main__":
    main()