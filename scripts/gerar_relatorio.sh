#!/bin/bash

# Período dos últimos 30 dias
DESDE=$(date -d "30 days ago" +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d)

echo "<h2>Commits por membro (últimos 30 dias)</h2>"
echo "<table><tr><th>Membro</th><th>Commits</th><th>Linhas +</th><th>Linhas -</th></tr>"

# Lista todos os autores e conta commits + diff
git log --since="$DESDE" --format="%ae" | sort | uniq | while read autor; do
  commits=$(git log --since="$DESDE" --author="$autor" --oneline | wc -l | tr -d ' ')
  
  # Linhas adicionadas e removidas por autor
  stats=$(git log --since="$DESDE" --author="$autor" --pretty=tformat: --numstat \
    | awk '{add+=$1; del+=$2} END {print add, del}')
  
  add=$(echo $stats | cut -d' ' -f1)
  del=$(echo $stats | cut -d' ' -f2)
  
  echo "<tr><td>$autor</td><td>$commits</td><td>+${add:-0}</td><td>-${del:-0}</td></tr>"
done

echo "</table>"

echo "<h2>Issues por tempo (via API GitHub)</h2>"
echo "<p><em>Veja o workflow para integração com GitHub Issues API</em></p>"