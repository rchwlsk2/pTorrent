import sys
import client.file_manager.MetadataFile as MetadataFile

##
# Tool to be able to generate a new metadata file
#
# @author Paul Rachwalski
# @date Apr 21, 2015
##

# Validate command line args
if len(sys.argv) != 2:
    print("Usage: " + sys.argv[0] + " <path to file>")
    sys.exit(0)

file_path = sys.argv[1]
metadata = MetadataFile()
metadata_path = metadata.generate(file_path, "54.200.76.207:6045", piece_size=1024*64)
print("Metadata file: " + metadata_path)
sys.exit(0)