# -*- coding: utf-8 -*-
"""Generate Rust sourcecode based on `contents.txt`

See below for the template strings that make up the Rust sourcecode.
`contents.txt` is based on the data form these two websites. See README.md
for more info.

- https://www.timetemperature.com/abbreviations/world_time_zone_abbreviations.shtml
- https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations#cite_note-17
"""

import collections

##############
# Constants  #
##############

# The file to read from
input_file = "content.txt"

# The file to write to
output_file = "src/generated.rs"

# The file content template
file_template = """
use phf::phf_map;
use crate::abbreviation::{{Abbreviation, Sign}};

pub(crate) static MAX_ABBREVIATION_LEN: usize = {max_len};

pub(crate) static ABBREVIATIONS: phf::Map<&'static str, &[Abbreviation]> = phf_map! {{
{content}
}};
"""

# The initialization template
init_template = """Abbreviation::new("{abbr}", "{name}", {sign}, {hour_offset}, {minute_offset})"""

# The join-abbreviations template
join_template = """  "{abbr}" => &[{collected}],"""


###################
# Implementation  #
###################

def write_items(abbreviation, entries):
    """Write a list of abbreviations into one key => Vec<Abbreviation> entry"""
    collected = []
    for name, sign, hour_offset, minute_offset in entries:
        tp_sign = "Sign::Plus" if sign == "+" else "Sign::Minus"
        collected.append(init_template.format(
            abbr=abbreviation.upper(), name=name, sign=tp_sign, hour_offset=hour_offset, minute_offset=minute_offset))
    joined = ", ".join(collected)
    tp_init = join_template.format(abbr=abbreviation.upper(), collected=joined)
    return tp_init


with open(output_file, "w") as output_fp:
    # Collect the abbreviation entries to join them in the end
    abbr_entries = []
    # The maximum length of an abbreviation. We use this as a library property.
    max_abbr_length = 0

    with open(input_file) as input_fp:
        entries = collections.OrderedDict()
        for line in input_fp.readlines():
            line = line.strip()

            # Ignore comments
            if len(line) == 0 or line[0] == "#":
                continue

            # Stop on Invalid lines
            components = line.split("\t")
            if len(components) != 3:
                print("Invalid line:", line)
                break
            abbreviation = components[0].lower()

            # DST as a timezone is `varied`. We ignore this one
            if abbreviation == "dst":
                continue

            # Retrive the components
            name = components[1].lower()
            timezone = components[2]

            # Convert "UTC + 3" or "UTC - 1" to ("+", 3) or ("-", 1)
            items = timezone.replace("UTC", "").strip().split(" ")
            if len(items) != 2 or not items[0] in ["+", "-"]:
                print("Invalid timezone info:", timezone, name)
                break
            sign = items[0]
            hour_offset = 0
            minute_offset = 0

            # Parse timezone with minute offsets (e.g `UTC + 10:30`)
            if items[1].find(":") != -1:
                c = items[1].split(":")
                if len(c) != 2:
                    print("Invalid timezone time:", items[1], name)
                    break
                hour_offset = int(c[0])
                minute_offset = int(c[1])
            else:
                hour_offset = int(items[1])

            if len(abbreviation) > max_abbr_length:
                max_abbr_length = len(abbreviation)

            # As we can have multiple timezones for one abbreviation, we collect
            # them.
            if not abbreviation in entries:
                entries[abbreviation] = [
                    (name, sign, hour_offset, minute_offset)]
            else:
                entries[abbreviation].append(
                    (name, sign, hour_offset, minute_offset))

        # Generate `struct` entries for each list of abbreviation items
        for key in entries:
            abbr_entries.append(write_items(key, entries[key]))

    # Write out
    content = "\n".join(abbr_entries)
    output_fp.write(file_template.format(
        content=content, max_len=max_abbr_length))
