> [!WARNING]
>
> This project is in early development and not yet functional.

# Cinemix

<a id="readme-top"></a>

<div align="center">
  <a href="https://github.com/Homies-Tech-Innovation/">
    <img src="./assets/logo.png" alt="Logo" width="100" height="100">
  </a>
  <h3 align="center">Cinemix</h3>
  <p align="center">
    Cinemix is a streamlined app for effortless discovery of movies and shows.
    <br />
    <br />
    <a href="./.github/ISSUE_TEMPLATE/bug_report.yml">
    Report a Bug
  </a>
  ·
  <a href="./.github/ISSUE_TEMPLATE/feature_request.yml">
    Request a Feature
  </a>
  ·
  <a href="./.github/contributing.md">
    View Contribution Guide
  </a>
  </p>
</div>

<div align="center">

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
[![License][license-shield]][license-url]
[![Discord][discord-shield]][discord-url]
[![Release][release-shield]][release-url]

</div>

## About The Project

<div align="center">
  <img src="./assets/image1.jpeg" alt="Project Banner" width="100%" style="max-width: 1200px;">
</div>

**Cinemix** is a backend-focused project designed to simplify and optimize the discovery of movies and TV shows through efficient data retrieval and processing. It interacts with external APIs to provide structured, searchable media data while maintaining speed, reliability, and scalability. This project serves as a learning platform for building robust backend services that handle real-world constraints like API limits and performance bottlenecks.

**Core Philosophy:**

- **Rate Limiting:** Ensures compliance with API usage restrictions while preventing service slowdowns by controlling request frequency.
- **Caching:** Stores frequently accessed data to reduce redundant API calls, improve response times, and enhance overall system efficiency.
- **Advanced Search:** Enables quick and flexible querying of movie and TV show data for more relevant and precise results.

### Built With

[![Python][Python]][Python-url]
[![FastAPI][FastAPI]][FastAPI-url]
[![Redis][Redis]][Redis-url]

## Getting Started

To get a local copy up and running, follow these simple steps.

### Prerequisites

Make sure you have Python 3.8+ and UV installed on your system.

- Install UV:
  ```sh
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

### Installation

1. Clone the repository to your local machine:

- ```sh
  git clone https://github.com/Homies-Tech-Innovation/cinemix.git
  cd cinemix
  ```

2. Install the required Python packages using UV:

- ```sh
  uv sync
  ```

3. Set up your environment variables by copying the sample file:

- ```sh
  cp .env.sample .env
  ```

4. Run the app:

- ```sh
  uv run -m src.main
  ```

## Usage

> [!CAUTION]
>
> This project is in active development. Expect frequent updates and possible instability.

- Usage will be documented once the project's stable version is released.

## Roadmap

Outline future plans and features for the project.

- **MVP:** Simple search for movies and shows with caching and rate limiting.
- **v2:** User accounts with Auth and wishlisting shows and movies.

See the open issues for a full list of proposed features (and known issues).

## Contributing

Contributions are the lifeblood of open source. Any contributions you make are greatly appreciated. Please read our **[Contribution Guide](./CONTRIBUTING.md)** for details on our code of conduct and the process for submitting pull requests.

## License

Distributed under the MIT License. See [`LICENSE`](./LICENSE) file for more information.

## Acknowledgments

- **[External API used](README.md#acknowledgments):** Cinemix is heavily dependent on the API, and we really appreciate its generous free tier.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<h1></h1>
<div align="center">
  <img src="https://github.com/aditsuru-git/readme-template/blob/main/assets/footer-team.png?raw=true" alt="Footer Banner" width="100%" style="max-width: 1200px;">
</div>

[contributors-shield]: https://img.shields.io/github/contributors/Homies-Tech-Innovation/cinemix
[contributors-url]: ./graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/Homies-Tech-Innovation/cinemix
[forks-url]: ./network/members
[stars-shield]: https://img.shields.io/github/stars/Homies-Tech-Innovation/cinemix
[stars-url]: ./stargazers
[issues-shield]: https://img.shields.io/github/issues/Homies-Tech-Innovation/cinemix
[issues-url]: ./issues
[license-shield]: https://img.shields.io/github/license/Homies-Tech-Innovation/cinemix
[license-url]: ./LICENSE
[discord-shield]: https://img.shields.io/discord/1313767817996402698?logo=discord&logoColor=white&label=discord&color=4d3dff
[discord-url]: https://discord.com/invite/HP2YPGSrWU
[release-shield]: https://img.shields.io/github/v/release/Homies-Tech-Innovation/cinemix?include_prereleases
[release-url]: ./releases
[FastAPI]: https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi
[FastAPI-url]: https://fastapi.tiangolo.com/
[Python]: https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54
[Python-url]: https://www.python.org/
[Redis]: https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white
[Redis-url]: https://www.python.org/
