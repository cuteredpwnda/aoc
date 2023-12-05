use criterion::{black_box, criterion_group, criterion_main, Criterion};
use day_04::{};

fn criterion_benchmark(c: &mut Criterion) {    
    c.bench_function("part_1", |b| b.iter(|| part_1(black_box(include_str!("../input/input.txt")))));
    c.bench_function("part_2", |b| b.iter(|| part_2(black_box(include_str!("../input/input.txt")))));
}

criterion_group!(benches, criterion_benchmark);
criterion_main!(benches);