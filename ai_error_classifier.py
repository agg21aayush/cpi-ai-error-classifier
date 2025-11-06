@app.post("/classifyError")
def classify_error(req: ErrorRequest):
    t = req.errorText.lower()

    def r(cat, conf, act): 
        return {"errorCategory": cat, "confidence": conf, "recommendedAction": act}

    if "401" in t or "unauthorized" in t:
        return r("Authentication", 0.95, "Renew access token or check credentials")
    if "timeout" in t or "sockettimeout" in t or "connection refused" in t:
        return r("Network", 0.9, "Check connectivity or retry after short delay")
    if "mapping" in t or "cannot convert" in t or "transformation" in t:
        return r("Mapping", 0.88, "Verify message mapping or payload structure")
    if "idoc" in t or "segment" in t or "edi_dc40" in t:
        return r("SAP IDoc", 0.85, "Validate IDoc structure and partner profiles")
    if "nullpointer" in t or "cannot read property" in t:
        return r("Runtime Null", 0.83, "Handle null checks and optional fields")
    if "sslhandshake" in t or "certificate" in t or "pkix path" in t:
        return r("SSL / Security", 0.9, "Verify certificates and truststore configuration")
    if "503" in t or "service unavailable" in t:
        return r("Receiver Unavailable", 0.87, "Retry after delay, check receiver status")
    if "500" in t or "soap:server" in t or "internal server error" in t:
        return r("Backend Error", 0.86, "Contact receiver application support")
    if "content-type" in t or "invalid json" in t or "invalid xml" in t:
        return r("Payload Format Error", 0.85, "Verify payload format and headers")
    if "duplicate" in t or "already processed" in t:
        return r("Duplicate Handling", 0.8, "Skip or suppress reprocessing")
    if "404" in t or "resource not found" in t or "unknown host" in t:
        return r("Configuration / Endpoint", 0.9, "Check endpoint URL or configuration")
    if "403" in t or "forbidden" in t or "access denied" in t:
        return r("Authorization", 0.9, "Review user permissions or roles")

    return r("Unknown", 0.6, "Manual investigation required")
