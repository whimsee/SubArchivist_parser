use std::env;
use std::fs;
use anyhow::Result;
use crunchyroll_rs::common::StreamExt;
use crunchyroll_rs::Crunchyroll;

#[tokio::main]
async fn main() -> Result<()> {

    let file_path = "src/user.txt";
    let file_path2 = "src/pass.txt";

    let user = fs::read_to_string(file_path)
        .expect("Should have been able to read the file");

    let pass = fs::read_to_string(file_path2)
        .expect("Should have been able to read the file");
    let email = user;
    let password = pass;
    // let email = env::var("EMAIL").expect("'EMAIL' environment variable not found");
    // let password = env::var("PASSWORD").expect("'PASSWORD' environment variable not found");

    let crunchyroll = Crunchyroll::builder()
        .login_with_credentials(email, password)
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