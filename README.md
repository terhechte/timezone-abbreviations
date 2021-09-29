# timezone-abbreviations

[![crates.io](https://img.shields.io/crates/v/timezone-abbreviations)](https://crates.io/crates/timezone-abbreviations)
[![docs.rs](https://docs.rs/timezone-abbreviations/badge.svg)](https://docs.rs/timezone-abbreviations/)

This crate allows converting between timezone abbreviations to timezone information.

[Note that timezone abbreviations are not standardized](https://stackoverflow.com/questions/56050292/is-there-a-way-to-parse-a-timezone-abbreviation-into-a-timezone-offset-in-rust):

> Keep in mind that time zone abbreviations are not standardized (Hawaii uses both HST or HAST), nor are they unique (CST could belong to US Central Standard Time, Cuba Standard Time, or China Standard TIme), nor do all time zones have abbreviations (many zones in the tzdb zones will just show abbreviations as offsets like "+02"). Also some languages use different abbreviations than we might use in English - example EST in English or HNE in French are both used in Canada for the same zone [Matt Johnson-Pint](https://stackoverflow.com/questions/56050292/is-there-a-way-to-parse-a-timezone-abbreviation-into-a-timezone-offset-in-rust#comment98768686_56050292)

The data in this crate is based on these two articles:

- [World Time Zone Abbreviations](https://www.timetemperature.com/abbreviations/world_time_zone_abbreviations.shtml)
- [Wikipedia](https://en.wikipedia.org/wiki/List_of_time_zone_abbreviations#cite_note-17)

The way it works is that the content of [this page](https://www.timetemperature.com/abbreviations/world_time_zone_abbreviations.shtml) with some manual additions and fixes from Wikipedia were manually downloaded into `content.txt`. Then, `generate.py` is used to generate `src/generated.rs` which contains a static hashmap of all the abbreviations.

This crate uses [PHF](https://github.com/rust-phf/rust-phf) for a very fast compile-time checked hashmap.

As a convenience, you can just call:

``` rs
let abbr = timezone_abbreviations::timezone("GMT")
```
