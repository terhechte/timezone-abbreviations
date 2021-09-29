/// The sign of the timezone
#[derive(Clone, Debug, Eq, PartialEq)]
pub enum Sign {
    Plus,
    Minus,
}

impl Sign {
    /// Return the `Sign` as a char. `+` or `-`
    pub fn as_char(&self) -> char {
        match &self {
            Sign::Plus => '+',
            Sign::Minus => '-',
        }
    }

    /// Return `true` if the sign is `Plus`
    pub fn is_plus(&self) -> bool {
        match &self {
            Sign::Plus => true,
            Sign::Minus => false,
        }
    }

    /// Return `true` if the sign is `Minus`
    pub fn is_minus(&self) -> bool {
        match &self {
            Sign::Plus => false,
            Sign::Minus => true,
        }
    }
}

/// A timezone abbreviation
#[derive(Clone, Debug, Eq, PartialEq)]
pub struct Abbreviation {
    /// The abbrevition, all lowercase
    pub abbr: &'static str,
    /// The name of the timezone
    pub name: &'static str,
    /// The sign. `+` or `-`
    pub sign: Sign,
    /// The timezone offset hours
    pub hour_offset: u8,
    /// The timezone offset minutes
    pub minute_offset: u8,
}

impl Abbreviation {
    pub(crate) const fn new(
        abbr: &'static str,
        name: &'static str,
        sign: Sign,
        hour_offset: u8,
        minute_offset: u8,
    ) -> Self {
        Abbreviation {
            abbr,
            name,
            sign,
            hour_offset,
            minute_offset,
        }
    }
}
