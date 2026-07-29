# STReamGT — Glossary

Plain definitions of the terms you'll meet in the app and in your results. Ordered roughly by where they turn up — from a physical kit through to a matched animal — not alphabetically.

------------------------------------------------------------------------

## The lab side

### Kit

A physical library you receive in the post: a 96-well (8×12) plate preloaded for one species, together with the barcodes and primers needed to sequence it. You fill the wells with your samples, run them, and upload the reads. In the app a kit already knows its species, **primer panel** and **tag** layout, so there's nothing to configure. A kit moves through statuses — **sent → received → analysed** (and **reanalyse** if you run it again). One kit = one library = up to 96 wells.

### Primer panel

The set of PCR primers a kit uses — one pair per **marker**. Panels are species-specific (e.g. `UA` for brown bear, `LL_MPA` for lynx) and decide which markers you get genotypes for. Sex and SNP markers also carry a reference sequence in the panel, so the caller knows what an X versus a Y, or each SNP allele, should look like.

### Tags (PP columns)

Short DNA barcodes attached to your fragments so a pooled sequencing run can be un-pooled afterwards. Each **PP column** is one physical primer plate carrying one set of tags. Because every well-and-plate combination gets a unique tag pair, the pipeline can take a pile of mixed reads and sort each one back to the exact well it came from. You choose which PP columns a batch uses when you submit.

### Replicates

The same sample amplified more than once — usually across several PP columns/wells. Noninvasive samples (scat, hair) give low-DNA, error-prone reads, so a single PCR can't be trusted. Replicates let the caller keep the alleles that show up repeatedly and drop the one-off artifacts. See **Consensus**.

### Controls

Wells with a known expected result, there to catch trouble:

-   **Negative controls** — a **blank** (no DNA) and a **PCRneg** (PCR with no template). They should come back empty; reads here mean contamination.
-   **Positive control** — a known reference animal that should reproduce a known genotype. If it doesn't, something in the run drifted.

Controls are typed (blank/sequencing, PCR, extraction, positive), coloured on the plate, and checked in the QC report. They are never treated as real animals.

------------------------------------------------------------------------

## The analysis

### Analysis (bioinformatics)

The automatic pipeline run that turns your raw reads into genotypes. It pairs and filters the reads, un-pools them by tag, calls alleles in every replicate, and builds a **consensus** per sample. You start it from the app — one submission is one **run** (a *job*) — and a couple of hours later you get result files and reports. No bioinformatics knowledge needed on your side.

### Reads / FASTQ

The sequencer's raw output: millions of short DNA sequences in `.fastq` files. This is what you upload; everything else is derived from it.

### Marker (locus)

One spot in the genome that gets genotyped — a microsatellite (STR) or a SNP. The panel lists them, and genotypes are reported per marker. A wolf panel might carry ~20 microsatellites plus a couple of sex markers.

### Allele

One version of a marker. Its real identity is its **DNA sequence**, not its name. Microsatellite alleles mostly differ by length (number of repeats), so they're named by fragment length — with a suffix (e.g. `142_2`) when two same-length sequences differ. For SNPs and sex markers the sequence itself is the allele. Allele **names are assigned per project** and can differ from the per-kit names in your raw result files, so always match on the sequence, not the name.

### Genotype

A sample's two alleles at a marker — two if heterozygous, one repeated if homozygous. Stitched across all markers, the multi-locus genotype is effectively a DNA fingerprint that identifies an individual. The **consensus genotype** is the version agreed across replicates.

### Consensus

The genotype the app keeps after weighing the replicates: an allele is accepted only when it appears in enough replicate wells (the homozygote / heterozygote thresholds). This is what separates a true allele from stutter or dropout, and it's what **matching** compares.

------------------------------------------------------------------------

## Organising your data

### Project

Your workspace for making sense of genotypes. A project owns the allele-name catalog, holds **populations** and **studies**, and is where you recompute consensus and run animal **matching**. Samples from many kits and runs can share one project, and you can share a project with colleagues. Kits don't belong to a project — their samples do, once you assign a run to one.

### Population

A group of animals treated as one gene pool — for example the Dinaric wolf population. Matching only compares samples **within the same population**, and allele frequencies and animal groupings are worked out per population. A sample with no population won't be matched.

### Study

A sampling effort inside a project — say "2025 winter monitoring" or a single field season. It groups samples and can be switched in or out of matching. Attaching a kit to a study drops that kit's samples into the study (and its population).

### Sample

One biological specimen — scat, hair, blood or tissue — that you genotyped. It came from a kit well via a run, lives in a project (usually a population and study too), and carries a consensus genotype, a QC verdict and a genetic sex. Controls are samples as well, just flagged and never matched.

### Animal (individual)

A single real animal, reconstructed after the fact by **matching**: samples whose genotypes agree closely enough are grouped as the same individual. One animal usually has several samples — the same wolf sampled at different times and places. This is the point of the whole workflow: turning a pile of scats into a count of individuals.

------------------------------------------------------------------------

## A few more you'll meet

### Matching

Comparing samples' genotypes within a population to decide which came from the same animal, allowing for a little genotyping error. The result is the animal groupings above.

### Sex marker

A locus that reveals genetic sex — either a shared X/Y primer whose X and Y sequences differ, or separate ZFX/ZFY primers. The caller reads which sequences amplified and reports male or female.

### QC (quality control)

The per-sample and per-run checks: how many wells amplified, allelic dropout, false alleles, reads per well, and how the controls performed. The QC report and the plate read-count view tell you whether to trust a genotype or repeat the sample.

### Claim code

The one-time code shipped with a kit that the buyer redeems to unlock it in their account — no admin step.
