---
type: maxos-workflow
name: Daily News Briefing
version: 1
status: draft
trigger:
  type: time
  schedule: 0 7 * * *
  inputs:
    site_one: https://www.nrk.no
    site_two: https://www.bbc.com/news
steps:
- id: step-1
  name: News Briefing
  provider: claude
  model: opus
  thinking: ''
  inputs:
  - trigger
  output:
    as: file
    format: md
    filename: morning_news_brief_{date}
  prompt: 'You have live web access. Fetch the front page of {site_one} and the front
    page of {site_two}. From each front page identify the top 5 headline stories (the
    most prominent news stories, not sports results, weather, or promos). For each
    story, open the article and write a 2-4 sentence summary in English covering what
    happened, who is involved, and why it matters. Then produce a Markdown morning
    briefing as your entire final output, structured exactly like this: a title line
    in the form: # Morning News Briefing - <today''s date>; then one section per site
    (## <site name>); under each section, each story as ### <headline> followed by
    the summary paragraph and the article link on its own line. If a site is unreachable,
    say so in one line under its section and continue with the other. Output ONLY
    the briefing markdown, no preamble or process notes.'
---

# Daily News Briefing

Trigger: time. Steps: News Briefing.

This is an example scheduled workflow. It is kept as `draft` in the public
template so a new workspace does not start a news schedule until the owner
explicitly enables it.
