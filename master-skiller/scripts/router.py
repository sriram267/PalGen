#!/usr/bin/env python3
"""
Master Skiller - Autonomous Skill Router & Pipeline Orchestrator
Cross-platform routing engine for querying 2,499+ skills, scoring relevance,
and generating multi-skill execution DAG pipelines.
"""

import sys
import os
import json
import re
import argparse
from math import log

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WORKSPACE_ROOT = os.path.dirname(BASE_DIR)
CATALOG_PATH = os.path.join(BASE_DIR, "catalog.json")
TAXONOMY_PATH = os.path.join(BASE_DIR, "taxonomy.json")

# Standard execution lifecycle order (earlier phases execute before later phases)
PHASE_ORDER = [
    ("Analysis & Research", ["multimodal-analysis", "debugging-incident-response"]),
    ("UX & Design System", ["ui-ux-design", "3d-immersive"]),
    ("Architecture & Implementation", ["frontend-engineering", "backend-api", "database-storage", "devops-cloud", "ai-agentic-systems", "browser-extensions", "search-indexing"]),
    ("Testing & QA", ["testing-qa"]),
    ("Security & Compliance", ["security-compliance"]),
    ("Growth, Copywriting & Final Audit", ["seo-growth-marketing", "git-workflow-versioning"])
]

def load_catalog():
    if not os.path.exists(CATALOG_PATH):
        print(f"Error: Catalog not found at {CATALOG_PATH}", file=sys.stderr)
        sys.exit(1)
    with open(CATALOG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def load_taxonomy():
    if not os.path.exists(TAXONOMY_PATH):
        return {}
    with open(TAXONOMY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

STOPWORDS = {
    'the', 'and', 'for', 'with', 'from', 'that', 'this', 'use', 'using', 'how', 
    'what', 'skill', 'agent', 'expert', 'guide', 'build', 'create', 'make', 'run',
    'app', 'want', 'need', 'please', 'help', 'code', 'let', 'get', 'set'
}

def tokenize(text):
    tokens = set(re.findall(r'[a-z0-9\-]{2,}', text.lower()))
    return tokens - STOPWORDS

def score_skill(skill, query_tokens, query_raw, flagships_set=None):
    name_tokens = tokenize(skill["id"] + " " + skill["name"])
    desc_tokens = tokenize(skill["description"])
    tags = set(skill.get("tags", []))
    domain = skill.get("domain", "")
    
    score = 0.0
    skill_id_clean = skill["id"].lower()
    
    # Exact full match in query
    if skill_id_clean in query_raw or skill["name"].lower() in query_raw:
        score += 150.0
        
    # Name tokens matching (highest weight)
    name_overlap = query_tokens & name_tokens
    score += len(name_overlap) * 45.0
    
    # Substring check for important words (e.g., '3d' in '3d-web-experience')
    for q_tok in query_tokens:
        if len(q_tok) >= 2 and q_tok in skill_id_clean:
            score += 25.0
            
    # Tag matches
    tag_overlap = query_tokens & tags
    score += len(tag_overlap) * 20.0
    
    # Description matches
    desc_overlap = query_tokens & desc_tokens
    score += len(desc_overlap) * 10.0
    
    # Flagship core bonus if there is any overlap
    if flagships_set and skill["id"] in flagships_set and (name_overlap or tag_overlap or desc_overlap):
        score += 60.0
        
    # Quality score contribution
    score += min(skill.get("score", 0.0) * 0.1, 30.0)
    
    if skill.get("has_scripts", False):
        score += 15.0
        
    return round(score, 2)
    # Base match components
    name_tokens = tokenize(skill["id"] + " " + skill["name"])
    desc_tokens = tokenize(skill["description"])
    tags = set(skill.get("tags", []))
    domain = skill.get("domain", "")
    
    score = 0.0
    
    # Direct exact phrase match in id or name
    if skill["id"] in query_raw or skill["name"].lower() in query_raw:
        score += 150.0
        
    # Exact token matches in ID/Name
    name_overlap = query_tokens & name_tokens
    score += len(name_overlap) * 35.0
    
    # Tag matches
    tag_overlap = query_tokens & tags
    score += len(tag_overlap) * 20.0
    
    # Description matches
    desc_overlap = query_tokens & desc_tokens
    score += len(desc_overlap) * 8.0
    
    # Domain relevance boost
    domain_tokens = tokenize(domain.replace('-', ' '))
    if query_tokens & domain_tokens:
        score += 15.0
        
    # Robustness quality bonus (scaled)
    score += min(skill.get("score", 0.0) * 0.1, 25.0)
    
    # Scripts availability bonus
    if skill.get("has_scripts", False):
        score += 10.0
        
    return round(score, 2)

def assign_phase(domain):
    for idx, (phase_name, domain_list) in enumerate(PHASE_ORDER):
        if domain in domain_list:
            return idx, phase_name
    return 2, "Architecture & Implementation"

def route_query(query, top_n=5, target_domain=None):
    catalog = load_catalog()
    query_raw = query.lower()
    query_tokens = tokenize(query_raw)
    
    scored = []
    taxonomy = load_taxonomy()
    flagships = set()
    for d_val in taxonomy.values():
        flagships.update(d_val.get("flagship", []))
        
    for s in catalog:
        if target_domain and s.get("domain") != target_domain:
            continue
        rel = score_skill(s, query_tokens, query_raw, flagships_set=flagships)
        if rel > 15.0: # threshold
            scored.append((rel, s))
            
    scored.sort(key=lambda x: x[0], reverse=True)
    results = [s for _, s in scored[:top_n]]
    
    # Build execution pipeline by phase ordering
    pipeline = []
    for s in results:
        phase_idx, phase_name = assign_phase(s.get("domain", ""))
        pipeline.append({
            "phase_index": phase_idx,
            "phase_name": phase_name,
            "skill_id": s["id"],
            "path": s["path"],
            "description": s["description"],
            "score": s["score"]
        })
        
    # Sort pipeline chronologically by phase index
    pipeline.sort(key=lambda x: (x["phase_index"], -x["score"]))
    
    return results, pipeline

def main():
    parser = argparse.ArgumentParser(description="Master Skiller CLI - Query and chain skills")
    parser.add_argument("query", nargs="*", help="User prompt or task description")
    parser.add_argument("--top", type=int, default=5, help="Number of top skills to return (default: 5)")
    parser.add_argument("--domain", type=str, default=None, help="Filter by domain")
    parser.add_argument("--json", action="store_true", help="Output JSON for automated agent calling")
    parser.add_argument("--list-domains", action="store_true", help="List all indexed domains")
    
    args = parser.parse_args()
    
    if args.list_domains:
        taxonomy = load_taxonomy()
        catalog = load_catalog()
        counts = {}
        for s in catalog:
            d = s.get("domain", "other")
            counts[d] = counts.get(d, 0) + 1
        print("\n=== Master Skiller Domains ===")
        for d, info in taxonomy.items():
            print(f"  • {d:30} : {counts.get(d, 0):4d} skills | {info.get('title', '')}")
        return
        
    query_str = " ".join(args.query).strip()
    if not query_str:
        print("Usage: python router.py '<your task or prompt>' [--top 5] [--json]")
        sys.exit(1)
        
    results, pipeline = route_query(query_str, top_n=args.top, target_domain=args.domain)
    
    if args.json:
        output = {
            "query": query_str,
            "top_skills": results,
            "pipeline": pipeline
        }
        print(json.dumps(output, indent=2))
        return
        
    print(f"\n🎯 Master Skiller Routing for: \"{query_str}\"")
    print(f"Found {len(results)} optimal skill matches across catalog.\n")
    
    print("┌── Recommended Execution Pipeline (Chronological Order)")
    for i, step in enumerate(pipeline, 1):
        print(f"│ Step {i}: [{step['phase_name']}]")
        print(f"│   Skill: {step['skill_id']}")
        print(f"│   Path : {step['path']}")
        print(f"│   Brief: {step['description'][:90]}...")
        if i < len(pipeline):
            print("│   ↓")
    print("└── Pipeline Ready.\n")

if __name__ == "__main__":
    main()
