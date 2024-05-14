for i in svg png pdf
    do echo $i
    npx  @mermaid-js/mermaid-cli@latest -i architecture.mmd -o architecture.$i
done