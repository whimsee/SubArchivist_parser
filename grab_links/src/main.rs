use crunchyroll_rs::{Crunchyroll, MediaCollection};
use crunchyroll_rs::parse::UrlType;

#[tokio::main]
async fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Log in to Crunchyroll with your email and password.
    // Support for username login was dropped by Crunchyroll on December 6th, 2023
    let crunchyroll = Crunchyroll::builder()
        .login_with_credentials("<email>", "<password>")
        .await?;

    let url = crunchyroll_rs::parse_url("https://www.crunchyroll.com/watch/GRDQPM1ZY/alone-and-lonesome").expect("url is not valid");
    if let UrlType::EpisodeOrMovie(media_id) = url {
        if let MediaCollection::Episode(episode) = crunchyroll.media_collection_from_id(media_id).await? {
            println!(
                "Url is episode {} ({}) of {} season {}",
                episode.episode_number,
                episode.title,
                episode.series_title,
                episode.season_number
            )
        }
    } else {
        panic!("Url is not a episode")
    }

    Ok(())
}