SELECT * 
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 3,4

SELECT * 
FROM PortfolioProjects..CovidVaccinations
ORDER BY 3,4

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 1,2

-- Looking at Total Cases vs. Total Deaths
-- Shows likehood of dying if you contract covid in your country
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS DeathPercentage
FROM PortfolioProjects..CovidDeaths
WHERE location = 'Kazakhstan'
WHERE continent IS NOT NULL
ORDER BY 1,2

-- Looking at Total Cases vs. Population
-- Shows what percentage of population got Covid
SELECT location, date, population, total_cases, (total_cases/population)*100 AS percent_population_infected
FROM PortfolioProjects..CovidDeaths
--WHERE location LIKE '%states%'
WHERE continent IS NOT NULL
ORDER BY 1,2

-- Looking at Countries with Highest Infection Rate compared to Population
SELECT location, population, MAX(total_cases) AS highest_infecction_count,
	MAX((total_cases/population))*100 AS percent_population_infected
FROM PortfolioProjects..CovidDeaths
--WHERE location LIKE '%states%'
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY percent_population_infected DESC

-- Showing Countries with Highest Death Count per Population
SELECT location, population, MAX(CAST(total_deaths AS INT)) AS total_death_count,
	MAX((CAST(total_deaths AS INT)/population))*100 AS percent_population_dead
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY percent_population_dead DESC

SELECT location, population, MAX(CAST(total_deaths AS INT)) AS total_death_count
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY total_death_count DESC

-- By continent
SELECT location, MAX(CAST(total_deaths AS INT)) AS total_death_count
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NULL
GROUP BY location
ORDER BY total_death_count DESC

SELECT continent, MAX(CAST(total_deaths AS INT)) AS total_death_count
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY continent
ORDER BY total_death_count DESC


-- Showing continents with the highest death coint per population
SELECT location, population, MAX(CAST(total_deaths AS INT)) AS total_death_count,
	MAX((CAST(total_deaths AS INT)/population))*100 AS percent_population_dead
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY percent_population_dead DESC


-- Global Numbers
SELECT date, SUM(new_cases) as total_cases,
	SUM(CAST(new_deaths AS INT)) as total_death,
	SUM(CAST(new_deaths AS INT))/SUM(new_cases)*100 AS death_percentage
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1,2

SELECT SUM(new_cases) as total_cases,
	SUM(CAST(new_deaths AS INT)) as total_death,
	SUM(CAST(new_deaths AS INT))/SUM(new_cases)*100 AS death_percentage
FROM PortfolioProjects..CovidDeaths
WHERE continent IS NOT NULL
ORDER BY 1,2


-- Looking at Total Population vs. Vaccination

-- USE CTE
WITH PopVsVac (continent, location, date, population, new_vaccinations, rolling_people_vaccinated)
AS (
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(CONVERT(INT, vac.new_vaccinations)) OVER 
	(PARTITION BY dea.location ORDER BY dea.location, dea.date) AS rolling_people_vaccinated
FROM PortfolioProjects..CovidDeaths dea 
JOIN PortfolioProjects..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL
)
SELECT *, (rolling_people_vaccinated/population)*100
FROM PopVsVac
ORDER BY 2,3

-- TEMP TABLE
DROP TABLE IF EXISTS #PERCENTPopulationVaccinated
CREATE TABLE #PERCENTPopulationVaccinated
(
continent nvarchar(255),
location nvarchar(255),
date datetime,
population numeric,
new_vaccinations numeric,
rolling_people_vaccinated numeric
)

INSERT INTO #PERCENTPopulationVaccinated
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(CONVERT(INT, vac.new_vaccinations)) OVER 
	(PARTITION BY dea.location ORDER BY dea.location, dea.date) AS rolling_people_vaccinated
FROM PortfolioProjects..CovidDeaths dea 
JOIN PortfolioProjects..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL

SELECT *, (rolling_people_vaccinated/population)*100
FROM #PERCENTPopulationVaccinated
ORDER BY 2,3


-- Creating View to store data for later visualizations
CREATE VIEW PercentPopulationVaccinated AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(CONVERT(INT, vac.new_vaccinations)) OVER 
	(PARTITION BY dea.location ORDER BY dea.location, dea.date) AS rolling_people_vaccinated
FROM PortfolioProjects..CovidDeaths dea 
JOIN PortfolioProjects..CovidVaccinations vac
	ON dea.location = vac.location
	AND dea.date = vac.date
WHERE dea.continent IS NOT NULL


SELECT *
FROM PercentPopulationVaccinated
ORDER BY 2,3