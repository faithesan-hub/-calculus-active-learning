# Publish guide

*Plain-language note: use this only after you have finished docs/VERIFY_CHECKLIST.md and Claude has rebuilt the final package. It walks you through putting the project online, getting its permanent DOI, and posting the paper. Total time: about 45 minutes. Do the steps in order.*

## Copy-ready text

**Title:** Active Learning in First-Semester Calculus: An Open Re-analysis of a Randomized Trial at a Hispanic-Serving Institution

**Author:** Faith Oluwafunmitan Esan, Independent Researcher, Laramie, Wyoming, USA. ORCID 0009-0001-3694-157X

**Short description (for GitHub and Zenodo):** Open, reproducible re-analysis of a randomized trial of active learning versus lecture in first-semester calculus (Kramer et al., 2023). Includes data cleaning, quality checks, analysis code, figures, and the manuscript.

**Abstract:** paste the final abstract from `paper/manuscript.pdf`.

**Keywords:** active learning; cooperative learning; calculus; randomized trial; mathematics education; open science; Hispanic-Serving Institutions

**AI disclosure (if asked):** Claude (Anthropic) assisted with writing analysis code, building figures, and drafting text. The author directed the analysis, checked every reported number against the data, and takes full responsibility for the content.

---

## Step 1. Put the project on GitHub (10 min)

1. Sign in at https://github.com and go to https://github.com/new.
2. **Repository name:** `calculus-active-learning`. **Description:** paste the short description. Choose **Public**. Leave "Add a README" **unticked**. Click **Create repository**.
3. On the next page, click the link **uploading an existing file**.
4. Unzip the project folder Claude gave you. Open it, select everything inside it (all files and folders), and drag them onto the GitHub page. Wait until every file is listed.
5. In "Commit changes", type `Version 0.1.0` and click **Commit changes**. You should now see the README displayed at the bottom of the repository page.

*Prefer Claude to do this?* Create a token at https://github.com/settings/tokens/new (tick **repo**, set expiry 7 days), and paste it when Claude asks. Delete it afterwards at the same page.

## Step 2. Get a permanent DOI from Zenodo (10 min)

1. Sign in at https://zenodo.org with **Log in with ORCID**.
2. Top right, click your name, then **GitHub**. Click **Sync now**. Find `faithesan-hub/calculus-active-learning` and flip its switch **On**.
3. Back on GitHub, open your repository, click **Releases** (right side), then **Create a new release**.
4. Click **Choose a tag**, type `v0.1.0`, click **Create new tag**. Title: `v0.1.0`. Description: paste the short description. Click **Publish release**.
5. Wait 2 to 5 minutes, then go to https://zenodo.org/me/uploads. Your project appears with a DOI that looks like `10.5281/zenodo.1234567`. Open it, click **Edit**, check that your name and ORCID are right, and **Publish** if asked.
6. Send the DOI to Claude. Claude puts it in the README, the citation file, and the paper.

## Step 3. Post the paper on EdArXiv (15 min)

EdArXiv is the free preprint server for education research, run on the OSF platform.

1. Go to https://edarxiv.org and click **Add a preprint**. Sign in with your ORCID (create the OSF account if asked; it is free).
2. Upload `paper/manuscript.pdf` (the final version Claude gives you).
3. Fill in: title, abstract, and keywords from the copy-ready text. Subject: **Education → Higher Education** and **Mathematics Education** if listed. License: **CC BY 4.0**.
4. Under "Supplemental materials" or "Link to data/code", paste your GitHub link and your Zenodo DOI.
5. Answer the conflict-of-interest question (none) and the data question (data and code are public, give the DOI).
6. Click **Submit**. Moderation takes a few days. Save the confirmation email.

## Step 4. Submit to a journal (later, 20 min)

Recommended: *International Journal of Research in Undergraduate Mathematics Education* (Springer). Use the standard subscription route, which has no publication fee; do not tick the open-access option unless you want to pay. Claude can prepare a cover letter and reformat the manuscript to the journal's style when you are ready.

## Step 5. Log it the same day (2 min each)

Add a row to your evidence log for each step: date, what was published, where, link or DOI, and save a PDF of the live page. Publications not logged the day they happen are the ones that go missing later.

```
date,artifact_or_event,type,venue_or_host,link_or_doi,status,prong_tags,metrics_snapshot,files_saved,notes
YYYY-MM-DD,Calculus active learning re-analysis v0.1.0,dataset+code,Zenodo + GitHub,10.5281/zenodo.NNNNNNN,live,,0 downloads at release,zenodo_record.pdf,Released after verification checklist completed
```
