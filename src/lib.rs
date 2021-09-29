mod abbreviation;
mod generated;

/// Return one or more timezones for the given timezone abbreviation.
/// Examples are `GMT` for Greenwich Mean Time or
/// `PST` for Pacific Standard Time.
/// Note that there is RFC for these abbreviations, which means that
/// some of them resolve to multiple different timezones. Hence this
/// function will return multiple [[`generated::Abbreviation`]] items.
pub fn timezone(abbr: &str) -> Option<&'static [abbreviation::Abbreviation]> {
    if let Some(n) = generated::ABBREVIATIONS.get(abbr) {
        Some(n)
    } else {
        None
    }
}

/// Return the maximum length that a timezone abbreviation can have.
/// This can be used to fetch the appropriate number of characters
/// from a string during parsing in order to identify a possible
/// timezone entry.
pub fn max_abbreviation_len() -> usize {
    generated::MAX_ABBREVIATION_LEN
}

#[cfg(test)]
mod tests {
    use super::timezone;
    #[test]
    fn it_works() {
        assert_eq!(timezone("PST").unwrap().first().unwrap().abbr, "PST");
        assert_eq!(timezone("GMT").unwrap().first().unwrap().abbr, "GMT");
        assert_eq!(timezone("XXWhat"), None);
    }
}
