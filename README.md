# Preprint claim audit

An offline static audit compares documented preprint-identifier claims with Python source evidence. It does not execute inspected code.

```
arxiv-validation-claim-audit audit [repo] [--json] [--verbose] [--ignore PREFIX] [--fail-on high|medium]
python3 -m arxiv_validation_claim_audit audit .
documented-arxiv-validation-claim-false
documented-no-arxiv-validation-claim-false
```

Findings fail at the selected severity; the default is high. Exit status 0 means pass, 2 means a finding meets the threshold, and 1 means a usage or I/O error. Test-only evidence produces a medium finding.

## Limitations

A normalisation call strips a leading scheme and never judges a string.

A conversion call builds a resolver address and never judges a string.

A network fetch asks a service for a record and never judges a string.

A direct pattern match is a shape check, not a library judgement.

A Handle call judges a wider namespace and is not recognised.

A DOI call judges a digital object identifier string and is not recognised.

A PMID call judges a medical record string and is not recognised.

The validators package does not provide the relevant route.

The stdnum package does not provide the relevant route.

Strings, comments, imports and bare references do not establish a call.

Syntax errors prevent source evidence.

Calls split across modules do not combine into evidence.

A subprocess invocation does not count.

Roadmap, changelog and TODO prose can produce claims without implemented code.

The library does not establish registration of any string.

There is no check digit: any string matching the shape passes.

A trailing space fails the shape check.

A trailing newline passes the shape check.

An embedded newline fails the shape check.

A leading space fails the shape check.

A missing sequence fails: 2101. is rejected.

A six digit sequence fails: 2101.123456 is rejected.

An empty string fails the shape check.

Uppercase letters pass: ARXIV:2101.12345 is accepted.

A subject class form passes: hep-th/2101.12345 is accepted.

A bare scheme form passes: arxiv:2101.12345 is accepted.

A single-character slip in the sequence still passes the shape check.

A four digit sequence passes: 2101.1234 is accepted.

Any year month passes: 9999.12345 is accepted.

A normalisation call returns a prefixed string for any input.

## Phrase hazards

```
validate arxiv
```

The bare phrase above can describe a manual runbook step.

```
arxiv validation
```

The bare phrase above can describe a roadmap feature.

```
arxiv validator
```

The bare phrase above can describe a hosted web page.

```
arxiv check
```

The bare phrase above can describe a field-presence lint rule.

```
check arxiv
```

The bare phrase above can describe a manual runbook step.

```
verify arxiv
```

The bare phrase above can describe a visual account confirmation.

```
arxiv validation check
```

The bare phrase above can describe a field-presence check.

```
valid arxiv
```

The bare phrase above can appear as example output.

```
arxiv is valid
```

The bare phrase above can appear as example error text.

```
arxiv is invalid
```

The bare phrase above can name a configuration flag or column.

```
arxiv validity
```

The bare phrase above can describe a format without code.

```
arxiv format validation
```

The bare phrase above can describe a shape-only check.

```
validate arxiv format
```

The bare phrase above can name a specification section.

```
validate arxiv id
```

The bare phrase above can describe a manual runbook step.

```
arxiv id validation
```

The bare phrase above can describe a manual runbook step.

```
check arxiv id
```

The bare phrase above can describe a manual runbook step.

```
verify arxiv id
```

The bare phrase above can name a specification section.

```
arxiv id check
```

The bare phrase above can name a reference-data checklist item.

```
arxiv id validation check
```

The bare phrase above can describe a result from an external platform.

```
arxiv id validator
```

The bare phrase above alone names a string without judging it.

```
arxiv
```

The bare phrase above alone does not claim a judgement.

```
arxiv id
```

The bare phrase above alone does not claim a judgement.

```
arxiv.org
```

The bare phrase above alone does not claim a judgement.

```
preprint
```

The bare phrase above alone does not claim a judgement.

```
subject class
```

The bare phrase above alone does not claim a judgement.

```
identifier
```

The bare phrase above alone does not claim a judgement.

```
sequence
```

The bare phrase above alone does not claim a judgement.

```
version
```

The bare phrase above alone does not claim a judgement.

## Matched phrases

```
validate arxiv
validates arxiv
validating arxiv
arxiv validation
arxiv validations
arxiv validator
arxiv validation check
arxiv check
check arxiv
verify arxiv
arxiv verification
arxiv is valid
arxiv is invalid
valid arxiv
invalid arxiv
arxiv validity
arxiv format validation
validate arxiv format
arxiv length validation
arxiv character validation
is valid arxiv
is arxiv valid
arxiv validation library
arxiv validation function
arxiv validation tool
checks arxiv
checking arxiv
verifies arxiv
verifying arxiv
validate arxiv id
validates arxiv id
validating arxiv id
arxiv id validation
arxiv id validations
arxiv id validator
arxiv id validation check
arxiv id check
check arxiv id
verify arxiv id
arxiv id verification
arxiv id is valid
arxiv id is invalid
valid arxiv id
invalid arxiv id
arxiv id validity
arxiv id format validation
validate arxiv id format
is valid arxiv id
is arxiv id valid
arxiv id validation library
no arxiv validation
does not validate arxiv
no arxiv validator
no arxiv validation check
does not support arxiv validation
without arxiv validation
arxiv validation not supported
arxiv validation not available
cannot validate arxiv
cannot check arxiv
does not check arxiv
no arxiv check
does not verify arxiv
no arxiv verification
arxiv validation not implemented
does not validate arxiv format
no arxiv id validation
does not validate arxiv id
no arxiv id validator
arxiv id validation not supported
cannot validate arxiv id
does not verify arxiv id
no arxiv id verification
arxiv id validation not implemented
```

```
arxiv
arxiv id
arxiv.org
preprint
subject class
identifier
sequence
version
```

## Differentiation

This audit does not cover fetching a preprint record over the network (the fetch family); reading a string out of text or a document (the extraction family); checking whether a string is a well-formed digital object identifier string (the doi family); checking whether a string is a well-formed handle-system string (the handle family); checking whether a string is a well-formed archival resource key (the ark family); checking whether a string is a well-formed uniform resource name (the urn family); checking whether a string is a well-formed medical record string (the pmid family); checking whether a string is a well-formed open-access record string (the pmcid family); checking whether a string is a well-formed text-content string (the istc family); checking whether a string is a well-formed science-resource string (the cstr family); checking whether a string is a well-formed research-organisation string (the ror family); checking whether a string is a well-formed openalex string (the openalex family); checking whether a string is a well-formed authority-file string (the viaf family); checking whether a string is a well-formed wikidata string (the wikidata family); checking whether a string is a well-formed authority record string (the gnd family); checking whether a string is a well-formed archive string (the hal family); checking whether a string is a well-formed software-heritage string (the swh family); checking whether a string is a well-formed research-resource string (the rrid family); checking whether a string is a well-formed six-letter classification string (the cfi family); checking whether a creditor-reference string is well-formed (the creditor-reference family); reading a classification string out of a document (the classification-code-extraction family); looking a string up by its classification code (the classification-code-lookup family); assigning a new classification code to a string (the classification-code-assignment family); checking whether input is checked at all (the generic validation family), checking whether a book number passes the ISBN-10 / ISBN-13 check digit (the ISBN-validation family), checking whether a serial number passes the ISSN check digit (the ISSN-validation family), checking whether a bank account number passes the IBAN check digit (the IBAN-validation family), checking whether a universally unique identifier string is well-formed (the UUID-validation family), checking whether a version string is a well-formed semantic version (the semver-validation family), checking whether a hardware address string is well-formed (the MAC-address-validation family), checking whether a business identifier code string is well-formed (the BIC-validation family), checking whether a cron-expression string is well-formed (the cron-expression-validation family), turning a cron-expression string into a human-readable sentence (the cron-expression-description family), checking whether anything runs on a schedule (the scheduled-execution family), checking whether a date string is well-formed (the date-validation family), checking whether a call times out (the timeout family), checking whether a payment is processed (the payment-processing family), reading a card number out of a document (the credit-card-extraction family), checking whether a user is authenticated (the auth family), hashing a password (the password-hashing family), generating a password (the password-generation family), encrypting a PDF (the PDF-encryption family), sending an email (the email-sending family), sending a text message (the SMS-sending family), reading data out of a document (the document-extraction family), scanning a barcode (the barcode-scanning family), checking whether an email address is well-formed (the email-validation family), checking whether a phone number is well-formed (the phone-validation family), checking whether a password is strong (the password-strength family), checking whether a document matches a JSON Schema (the JSON-Schema-validation family), checking whether a card number is well-formed (the credit-card-validation family), checking whether a domain name is well-formed (the domain-validation family), checking whether a URL is well-formed (the URL-validation family), checking whether an IP address is well-formed (the IP-validation family), parsing JSON (the JSON-parsing family), matching a regular expression (the regex family), parsing a URL (the URL-parsing family), fetching a URL (the URL-fetching family), resolving a domain name (the DNS family), generating a barcode (the barcode-generation family), reading an account number out of a document (the account-extraction family), reading a vehicle identification number out of a document (the VIN-extraction family), decoding a vehicle identification number (the VIN-decoding family), looking up a vehicle identification number's history (the VIN-history-lookup family), checking whether a hex color string is well-formed (the hex-color-validation family), checking whether a researcher identifier string is well-formed (the ORCID-validation family), checking whether a name identifier string is well-formed (the ISNI-validation family), checking whether a chemical registry number string is well-formed (the CASRN-validation family), checking whether a stock-exchange identifier string is well-formed (the SEDOL-validation family), checking whether a securities identifier string is well-formed (the ISIN-validation family), looking up a securities identifier's record (the ISIN-record-query family), reading a securities identifier out of a document (the ISIN-extraction family), checking whether a security identifier string is well-formed (the CUSIP-validation family — a CUSIP is a 9-character security identifier with a mod-10 check digit, and judging one says nothing about an arXiv ID), checking whether a device identifier string is well-formed (the IMEI-validation family), checking whether a mobile equipment identifier string is well-formed (the MEID-validation family), checking whether a legacy mobile equipment identifier string is well-formed (the ESN-validation family), checking whether a music number string is well-formed (the ISMN-validation family), checking whether an audiovisual number string is well-formed (the ISAN-validation family), checking whether a release identifier string is well-formed (the GRid-validation family), checking whether a barcode number string is well-formed (the EAN-validation family), checking whether a serial number string is well-formed (the generic-serial-number family), checking whether a financial instrument identifier string is well-formed (the FIGI-validation family), looking up a financial instrument identifier's record (the FIGI-record-query family), reading a financial instrument identifier out of a document (the FIGI-extraction family), checking whether a recording code string is well-formed (the ISRC-validation family), checking whether an Ethereum address string is well-formed (the Ethereum-address-validation family), checking whether a Binance Smart Chain address string is well-formed (the Binance-Smart-Chain-address-validation family), checking whether a Tron address string is well-formed (the Tron-address-validation family), checking whether a Litecoin address string is well-formed (the Litecoin-address-validation family), checking whether a Dogecoin address string is well-formed (the Dogecoin-address-validation family), checking whether a bitcoin address string is well-formed (the bitcoin-address-validation family), checking whether a transaction hash string is well-formed (the transaction-hash-validation family), checking whether a private key string is well-formed (the private-key-validation family), looking up a balance or transactions on a block explorer (the block-explorer family), generating an address (the address-generation family), reading an address out of a document (the address-extraction family), confirming receipt of a payment (the payment-receipt family), reading a spreadsheet (the spreadsheet-reading family), generating a spreadsheet (the spreadsheet-generation family), reading a Word document (the Word-reading family), generating a Word document (the Word-generation family), reading a presentation (the presentation-reading family), generating a presentation (the presentation-generation family), extracting text from a PDF (the PDF-extraction family), generating a PDF (the PDF-generation family), merging PDFs (the PDF-merging family), splitting a PDF (the PDF-splitting family), rotating a PDF (the PDF-rotation family), filling a PDF form (the PDF-form-filling family), watermarking a PDF (the PDF-watermarking family), redacting a PDF (the PDF-redaction family), compressing a PDF (the PDF-compression family), annotating a PDF (the PDF-annotation family), extracting a table (the table-extraction family), reading text from an image (the OCR family), extracting data from a document (the document-data-extraction family), signing a document electronically (the e-signature family), recording a screen (the screen-recording family), generating a video (the video-generation family), generating a QR code (the QR-generation family), generating a barcode (the barcode-generation family), scanning a barcode (the barcode-scanning family), mixing audio (the audio-mixing family), generating audio (the audio-generation family), editing audio (the audio-editing family), separating audio sources (the audio-source-separation family), recognising speech (the speech-recognition family), synthesising speech (the speech-synthesis family), reducing noise (the noise-reduction family), generating music (the music-generation family), transcribing music (the music-transcription family), checking whether a chemical identifier string is well-formed (the InChI family), checking whether a chemical notation string is well-formed (the SMILES family), checking whether a European Community number string is well-formed (the EC-number family), checking whether a United Nations transport number string is well-formed (the UN-transport-number family), looking up a compound in PubChem (the PubChem-query family), checking whether a chemical structure is well-formed (the chemical-structure-validation family), checking whether any other chemical identifier string is well-formed (the other-chemical-identifiers family), reading a container number out of a shipping document (the container-number-reading family), looking up a carrier registration by container number (the carrier-registry family), checking whether a shipowner code is registered (the BIC-shipowner-code family), checking whether a container size-type code is well-formed (the container-size-type family), generating a new container number (the container-number-generation family), checking whether a container number string is well-formed (the ISO-6346-validation family), fetching a library's record from a registry over the network (the library-record-fetching family), registering a new library identifier with an agency (the library-identifier-registration family), cataloguing a library collection or reading a MARC record (the cataloguing family), looking a library up in OCLC or WorldCat (the OCLC-WorldCat family), listing the agencies that issue library identifiers (the library-agency-listing family), checking whether a library-identifier string is well-formed (the ISIL-validation family), checking whether a ship-number string is well-formed (the IMO-validation family), checking whether a maritime mobile identity string is well-formed (the MMSI-validation family), checking whether a hull identification number string is well-formed (the HIN-validation family), checking whether a European vessel number string is well-formed (the ENI-validation family), looking a vessel up in a ship registry (the vessel-registry-lookup family), tracking a vessel by AIS (the AIS-tracking family), looking a ship up by name (the ship-name-lookup family), checking whether a subscriber-identity string is well-formed (the IMSI-validation family), looking a tax identifier up in the EU VIES registry over the network (the VIES-lookup family — a registry query, not a string judgement), looking up the tax rate for a country (the VAT-rate-lookup family), computing tax amounts on an invoice (the tax-calculation family), generating an invoice document (the invoice-generation family), checking whether a tax-identifier string is well-formed (the VATIN-validation family — a VATIN is a country code plus a country-specific identifier, and judging one says nothing about an arXiv ID), checking whether a SEPA structured creditor reference string is well-formed (the SEPA-creditor-reference family — an RF reference judged by the ISO 11649 check, a different identifier from an arXiv ID), reading an unstructured invoice or payment reference out of a document (the invoice-reference-extraction family), looking a payment up by its creditor reference (the payment-lookup family — a registry query, not a string judgement), generating a new creditor reference (the creditor-reference-generation family — minting a fresh string never judges an existing one), checking whether a classification code string is well-formed (the financial-instrument-classification family — a six-letter ISO 10962 code judged by a classification table, and judging one says nothing about an arXiv ID), checking whether a digital object identifier string is well-formed (the digital-object-identifier family — a "10."-prefixed registrant code plus a slash plus a suffix, and judging one says nothing about an arXiv ID).
