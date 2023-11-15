FROM haskell:slim

COPY main.hs .

RUN ghc -o main main.hs

ENTRYPOINT ["./main"]
