use std::fs;
use anyhow::Result;
use crunchyroll_rs::common::StreamExt;
use crunchyroll_rs::Crunchyroll;
use std::fmt;
// use crunchyroll_rs::media::Subtitle;
// use crunchyroll::Locale;

pub enum Locale {
    ar_ME,
    ar_SA,
    ca_ES,
    de_DE,
    en_IN,
    en_US,
    es_419,
    es_ES,
    es_LA,
    fr_FR,
    hi_IN,
    id_ID,
    it_IT,
    ja_JP,
    ko_KR,
    ms_MY,
    pl_PL,
    pt_BR,
    pt_PT,
    ru_RU,
    ta_IN,
    te_IN,
    th_TH,
    tr_TR,
    vi_VN,
    zh_CN,
    zh_HK,
    zh_TW,
    Custom(String),
}

impl fmt::Display for Locale {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{}", self)
    }
}

pub trait Summary {
    fn summarize(&self) -> String;
}

pub struct Subtitle {
    pub locale: Locale,
    pub url: String,
    pub format: String,
    /* private fields */
}

impl Summary for Subtitle {
    fn summarize(&self) -> String {
        format!("{}, by {} ({})", self.locale.to_string(), self.url, self.format)
    }
}

#[tokio::main]
async fn main() -> Result<()> {

    let file_path = "src/user.txt";
    let file_path2 = "src/pass.txt";

    let user = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let pass = fs::read_to_string(file_path2)
        .expect("Should have been able to read the file");

    let crunchyroll = Crunchyroll::builder()
        .login_with_credentials(user, pass)
        .await?;

    let mut query_result = crunchyroll.query("darling");
    while let Some(s) = query_result.series.next().await {
        let series = s?;

        println!(
            "Queried series {} which has {} seasons",
            series.title, series.season_count
        );
        let seasons = series.seasons().await?;
        for season in seasons {
            println!(
                "Found season {} with audio locale(s) {}",
                season.season_number,
                season
                    .audio_locales
                    .iter()
                    .map(|l| l.to_string())
                    .collect::<Vec<String>>()
                    .join(", ")
            )
        }
    }

    Ok(())
}